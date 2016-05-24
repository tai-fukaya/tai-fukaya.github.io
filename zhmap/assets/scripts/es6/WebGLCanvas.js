import THREE from 'three';
import LatLngVisualizer from './LatLngVisualizer';

export default class WebGLCanvas {
	constructor(w, h, $) {
		this.width = w;
		this.height = h;
		this.cameraFov = 60;
		let cameraZpos = this.height / 2 * Math.sqrt(3);

		// レンダラ
		this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
		this.renderer.setSize(this.width, this.height);
		this.renderer.setClearColor(0x000000, 0);
		this.renderer.domElement.style.position = "fixed";
		this.renderer.domElement.style.top = 0;
		this.renderer.domElement.style.left = 0;

		// シーン
		this.scene = new THREE.Scene();

		// カメラ
		this.camera = new THREE.PerspectiveCamera(this.cameraFov, this.width / this.height, 0.1, 1000);
		this.camera.position.z = cameraZpos;

		this.visualizer = new LatLngVisualizer(w, h, $);
		this.scene.add(this.visualizer);
	}

	animate() {
		this.renderer.render(this.scene, this.camera);
	}

	resize(width, height) {
		this.width = width;
		this.height = height;

		this.camera.aspect = width / height;
		this.camera.position.z = height / 2 * Math.sqrt(3);
		this.camera.updateProjectionMatrix();

		this.renderer.setSize(width, height);
		this.visualizer.resize(width, height);
	}
};