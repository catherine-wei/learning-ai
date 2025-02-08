import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { VRMLoaderPlugin, VRMUtils } from '@pixiv/three-vrm';
import { loadMixamoAnimation } from './loadMixamoAnimation.js';
import GUI from 'three/addons/libs/lil-gui.module.min.js';

export class ThreeVRMViewer {
	scene = null;

    constructor() {
        // renderer
        this.renderer = new THREE.WebGLRenderer();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);

        // document.body.appendChild(this.renderer.domElement);
        const liveArea = document.getElementById('liveArea');
        liveArea.innerHTML = "";
		liveArea.appendChild(this.renderer.domElement);

        // camera
        this.camera = new THREE.PerspectiveCamera(30.0, window.innerWidth / window.innerHeight, 0.1, 20.0);
        this.camera.position.set(0.0, 1.0, 5.0);

        // camera controls
        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.controls.screenSpacePanning = true;
        this.controls.target.set(0.0, 1.0, 0.0);
        this.controls.update();

        // scene
        this.scene = new THREE.Scene();

        // light
        this.light = new THREE.DirectionalLight(0xffffff, Math.PI);
        this.light.position.set(1.0, 1.0, 1.0).normalize();
        this.scene.add(this.light);

        this.defaultModelUrl = '/static/models/xiaomei2.vrm';
		this.defaultBackground = '/static/background/nex3.png';

        // gltf and vrm
        this.currentVrm = undefined;
        this.currentAnimationUrl = "/static/fbx/idle-female.fbx";
        this.currentMixer = undefined;

        this.helperRoot = new THREE.Group();
        this.helperRoot.renderOrder = 10000;
        // this.scene.add( this.helperRoot );

        this.params = { timeScale: 1.0, };

        // // gui
        // this.gui = new GUI();
        // this.gui.add(this.params, 'timeScale', 0.0, 2.0, 0.001).onChange((value) => {
        //     if (this.currentMixer) {
        //         this.currentMixer.timeScale = value;
        //     }
        // });

        // clock
        this.clock = new THREE.Clock();

        // add dnd event listeners
        this.addDragAndDropListeners();
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

                if (this.currentVrm) {
                    this.scene.remove(this.currentVrm.scene);
                    VRMUtils.deepDispose(this.currentVrm.scene);
                }

                this.currentVrm = vrm;
                this.scene.add(vrm.scene);

                vrm.scene.traverse((obj) => {
                    obj.frustumCulled = true;
                });

                if (this.currentAnimationUrl) {
                    this.loadFBX(this.currentAnimationUrl);
                }

                VRMUtils.rotateVRM0(vrm);

                console.log(vrm);
            },
            (progress) => console.log('Loading model...', 100.0 * (progress.loaded / progress.total), '%'),
            (error) => console.error(error)
        );
    }

    loadFBX(animationUrl) {
        this.currentAnimationUrl = animationUrl;

        if (this.currentVrm) {
            this.currentVrm.humanoid.resetNormalizedPose();
            this.currentMixer = new THREE.AnimationMixer(this.currentVrm.scene);

            loadMixamoAnimation(animationUrl, this.currentVrm).then((clip) => {
                if (this.currentMixer) {
                    this.currentMixer.clipAction(clip).play();
                    this.currentMixer.timeScale = this.params.timeScale;
                }
            });
        }
    }

	updateBackground(url) {
		// 使用 TextureLoader 加载背景图片
		const loader = new THREE.TextureLoader();
		loader.load(url, (texture) => {
			// 显式设置背景颜色为黑色
			// this.scene.background = new THREE.Color(0x000000);

			// 设置场景的背景为加载的纹理
			this.scene.background = texture;
		});
	}

    animate() {
        requestAnimationFrame(() => this.animate());
        const deltaTime = this.clock.getDelta();
        if (this.currentMixer) {
            this.currentMixer.update(deltaTime);
        }

        if (this.currentVrm) {
            this.currentVrm.update(deltaTime);
        }

        this.renderer.render(this.scene, this.camera);
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

    start() {
        this.loadVRM(this.defaultModelUrl);
		this.updateBackground(this.defaultBackground);
        this.animate();
    }
}
