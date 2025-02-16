import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { VRMLoaderPlugin, VRMUtils } from '@pixiv/three-vrm';
import { loadMixamoAnimation } from './loadMixamoAnimation.js';
import { LipSync } from './lipSync.js';
import { EmoteController } from "./emoteController.js";

export class ThreeVRMViewer {
	scene = null;

    constructor() {
        this.defaultModelUrl = '/static/models/xiaomei2.vrm';
		this.defaultBackground = '/static/background/nex3.png';
		this.defaultBackground = '/static/background/bg1.jpg';
        this.defaultAnimationUrl = "/static/fbx/idle-female.fbx";
        this.currentAnimationUrl = "/static/fbx/idle-female.fbx";

        // document.body.appendChild(this._renderer.domElement);
        const liveArea = document.getElementById('liveContainer');
        liveArea.innerHTML = "";
        const rect = liveArea.getBoundingClientRect();
        const width = rect.width;
        const height =  window.innerWidth/window.innerHeight * width;
        console.log("liveArea:" + width + "-" + rect.height + ", height: " + height);
        
        // renderer
        this._renderer = new THREE.WebGLRenderer();
        this._renderer.setSize(width, height);
        this._renderer.setPixelRatio(window.devicePixelRatio);
        
        liveArea.appendChild(this._renderer.domElement);

        // camera
        this._camera = new THREE.PerspectiveCamera(30.0, width / height, 0.1, 20.0);
        this._camera.position.set(0.0, 1.0, 5.0);

        // camera controls
        this._controls = new OrbitControls(this._camera, this._renderer.domElement);
        this._controls.screenSpacePanning = true;
        this._controls.target.set(0.0, 1.0, 0.0);
        this._controls.update();

        // scene
        this._scene = new THREE.Scene();

        // light
        this._light = new THREE.DirectionalLight(0xffffff, Math.PI);
        this._light.position.set(1.0, 1.0, 1.0).normalize();
        this._scene.add(this._light);

        // gltf and vrm
        this._currentVrm = undefined;
        this._currentMixer = undefined;

        this.helperRoot = new THREE.Group();
        this.helperRoot.renderOrder = 10000;
        // this._scene.add( this.helperRoot );

        this._params = { timeScale: 1.0, };

        // clock
        this._clock = new THREE.Clock();

        // add dnd event listeners
        this.addDragAndDropListeners();

        // emotion and lipSync
        this._lookAtTargetParent = this._camera;
        this._lipSync = new LipSync(new AudioContext());

        // auto adjust when window resized
        window.addEventListener("resize", () => {
            this.resize();
          });
    }

    /**
     * 参照canvas的父元素调整大小
     */
    resize() {
        if (!this._renderer) return;

        const parentElement = this._renderer.domElement.parentElement;
        if (!parentElement) return;

        this._renderer.setPixelRatio(window.devicePixelRatio);
        this._renderer.setSize(
            parentElement.clientWidth,
            parentElement.clientHeight
        );

        if (!this._camera) return;
        this._camera.aspect =
          parentElement.clientWidth / parentElement.clientHeight;
        this._camera.updateProjectionMatrix();
    }

    loadVRM(modelUrl) {
        const loader = new GLTFLoader();
        loader.crossOrigin = 'anonymous';

        this.helperRoot.clear();

        loader.register((parser) => {
            return new VRMLoaderPlugin(parser, { helperRoot: this.helperRoot });
        });

        loader.load(
            modelUrl,
            (gltf) => {
                const vrm = gltf.userData.vrm;

                VRMUtils.removeUnnecessaryVertices(gltf.scene);
                VRMUtils.combineSkeletons(gltf.scene);
                VRMUtils.combineMorphs(vrm);

                if (this._currentVrm) {
                    this._scene.remove(this._currentVrm.scene);
                    VRMUtils.deepDispose(this._currentVrm.scene);
                }

                this._currentVrm = vrm;
                this._scene.add(vrm.scene);

                vrm.scene.traverse((obj) => {
                    obj.frustumCulled = true;
                });

                if (this.currentAnimationUrl) {
                    this.loadFBX(this.currentAnimationUrl);
                }

                VRMUtils.rotateVRM0(vrm);
                this._emoteController = new EmoteController(vrm, this._lookAtTargetParent);
            
                console.log(vrm);
            },
            (progress) => console.log('Loading model...', 100.0 * (progress.loaded / progress.total), '%'),
            (error) => console.error(error)
        );
    }

    loadFBX(animationUrl) {
        this.currentAnimationUrl = animationUrl;

        if (this._currentVrm) {
            this._currentVrm.humanoid.resetNormalizedPose();
            this._currentMixer = new THREE.AnimationMixer(this._currentVrm.scene);

            loadMixamoAnimation(animationUrl, this._currentVrm).then((clip) => {
                if (this._currentMixer) {
                    this._currentMixer.clipAction(clip).play();
                    this._currentMixer.timeScale = this._params.timeScale;
                }
            });
        }
    }

	updateBackground(url) {
		// 使用 TextureLoader 加载背景图片
		const loader = new THREE.TextureLoader();
		loader.load(url, (texture) => {
			// 显式设置背景颜色为黑色
			// this._scene.background = new THREE.Color(0x000000);

			// 设置场景的背景为加载的纹理
			this._scene.background = texture;
		});
	}

    animate() {
        requestAnimationFrame(() => this.animate());
        const deltaTime = this._clock.getDelta();
        if (this._currentMixer) {
            this._currentMixer.update(deltaTime);
        }

        if (this._currentVrm) {
            this._currentVrm.update(deltaTime);
        }

        this._renderer.render(this._scene, this._camera);
    }

    addDragAndDropListeners() {
        window.addEventListener('dragover', (event) => {
            event.preventDefault();
        });

        window.addEventListener('drop', (event) => {
            event.preventDefault();
            const files = event.dataTransfer.files;
            if (!files) return;

            const file = files[0];
            if (!file) return;

            const fileType = file.name.split('.').pop();
            const blob = new Blob([file], { type: 'application/octet-stream' });
            const url = URL.createObjectURL(blob);

            if (fileType === 'fbx') {
                this.loadFBX(url);
            } else {
                this.loadVRM(url);
            }
        });
    }

    /**
     * 播放声音，进行唇部同步
     */
    async speak(buffer, screenplay) {
        this._emoteController?.playEmotion(screenplay.expression);
        await new Promise((resolve) => {
            this._lipSync?.playFromArrayBuffer(buffer, () => {
                resolve(true);
                this._emoteController?.playEmotion("neutral");
            });
        });
    }

    async playEmotion(emotionType) {
        this._emoteController?.playEmotion(emotionType);
    }

    async playAction(fbxUrl, once) {
        this.currentAnimationUrl = fbxUrl;

        if (this._currentVrm) {
            this._currentVrm.humanoid.resetNormalizedPose();
            this._currentMixer = new THREE.AnimationMixer(this._currentVrm.scene);
    
            loadMixamoAnimation(fbxUrl, this._currentVrm).then((clip) => {
                if (this._currentMixer) {
                    // 动画只播放一次，或者循环播放
                    if (once) {
                        // 创建动画动作
                        const action = this._currentMixer.clipAction(clip);
        
                        // 设置动画只播放一次
                        action.setLoop(THREE.LoopOnce, 1); // THREE.LoopOnce 表示只播放一次
                        action.clampWhenFinished = true; // 播放结束后停留在最后一帧
        
                        // 播放动画
                        action.play();
        
                        // 设置时间缩放
                        this._currentMixer.timeScale = this._params.timeScale;
        
                        // 监听动画结束事件
                        this._currentMixer.addEventListener('finished', (e) => {
                            console.log('Animation finished, restore to default animation');
                            // 一次性的动作完成后，恢复到默认的动作
                            this.loadFBX(this.defaultAnimationUrl);
                        });
                    } else {
                        this._currentMixer.clipAction(clip).play();
                        this._currentMixer.timeScale = this._params.timeScale;
                    }
                }
            });
        }
    }

    update(delta) {
        if (this._lipSync) {
          const { volume } = this._lipSync.update();
          this._emoteController?.lipSync("aa", volume);
        }
    
        this._emoteController?.update(delta);
        this._currentMixer?.update(delta);
        this._currentVrm?.update(delta);
    }

    start() {
        this.loadVRM(this.defaultModelUrl);
		this.updateBackground(this.defaultBackground);
        this.animate();
    }
}
