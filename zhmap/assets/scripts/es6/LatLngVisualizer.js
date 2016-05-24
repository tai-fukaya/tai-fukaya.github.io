import THREE from 'three';
import settings from './setting';

/**
 * this is THREE.LatLngVisualizer description.
 * 
 */
export default class LatLngVisualizer extends THREE.Object3D {
	/**
	 * this is MyClass constructor description.
	 * @param {string} [name="anonymous"] - this is name description.
	 */
	constructor(w, h, $) {
		super();

		let filePaths = settings.jsonurl;
		let completed = 0;
		let self = this;

		this.data = [];
		this.width = w;
		this.height = h;

		// 全部読み込む
		filePaths.forEach((filePath) => {
			$.getJSON(filePath, (data) => {
				self.data = self.data.concat(data);
				if (++completed === filePaths.length) {
					console.log(self.data.length);
					self.initializeGeometryColors();
					self.calculateGeometryPositions();
				}
			});
		});

		let geometry = new THREE.BufferGeometry();
		let material = new THREE.PointsMaterial({
			size: 2,
			blending: THREE.AdditiveBlending,
			vertexColors: THREE.VertexColors,
			opacity: 0.8,
			depthTest: false,
			transparent: true
		});
		let particle = new THREE.Points(geometry, material);
		particle.position.x = -w / 2;
		particle.position.y = -h / 2;
		particle.visible = false;
		this.particle = particle;

		this.add(this.particle);
	}
	initializeGeometryColors() {
		let colors = new Float32Array(this.data.length * 3);
		this.data.forEach((data, i) => {
			let baseId = i * 3;
			colors[baseId + 0] = colors[baseId + 1] = colors[baseId + 2] = 1.0;
		});
		this.particle.geometry.addAttribute('color', new THREE.BufferAttribute(colors, 3));
	}
	calculateGeometryPositions() {

		let self = this;

		// 最大値最小値の設定
		let maxLat = 0, minLat = 1000000,
			maxLng = 0, minLng = 1000000;
		self.data.forEach((data, index) => {
			if (data.lat === 0 && data.lng === 0) {
				self.data.splice(index, 1);
				return;
			}
			if (maxLat < data.lat) {
				maxLat = data.lat;
			}
			if (minLat > data.lat) {
				minLat = data.lat;
			}
			if (maxLng < data.lng) {
				maxLng = data.lng;
			}
			if (minLng > data.lng) {
				minLng = data.lng;
			}
		});
		// console.log(maxLat, minLat, maxLng, minLng);
		maxLat = ((((maxLat + 2) / 2) | 0) * 2);
		minLat = ((((minLat - 2) / 2) | 0) * 2);
		maxLng = ((((maxLng + 2) / 2) | 0) * 2);
		minLng = ((((minLng - 2) / 2) | 0) * 2);
		// console.log(maxLat, minLat, maxLng, minLng);

		let max = self.data.length;
		let lngSize = self.width / (maxLng - minLng);
		let latSize = self.height / (maxLat - minLat);

		let size = lngSize;
		if (latSize < size) {
			size = latSize;
		}
		let marginLeft = (self.width - (maxLng - minLng) * size) / 2,
			marginTop = (self.height - (maxLat - minLat) * size) / 2;

		console.log(self.width, marginLeft, self.height, marginTop, lngSize, latSize, size);
		// ポジションの設定
		let positions = new Float32Array(max * 3);
		self.data.forEach((data, i) => {
			let baseId = i * 3;
			positions[baseId + 0] = marginLeft + (data.lng - minLng) * size;
			positions[baseId + 1] = marginTop + (data.lat - minLat) * size;
			positions[baseId + 2] = 0;

		});

		self.particle.geometry.addAttribute('position', new THREE.BufferAttribute(positions, 3));

		self.particle.position.x = -self.width / 2;
		self.particle.position.y = -self.height / 2;
		self.particle.visible = true;
	}
	search(key) {
		let ret = {};
		if (!this.particle.visible) {
			return ret;
		}
		let colors = new Float32Array(this.data.length * 3);
		this.data.forEach((data, i) => {
			let baseId = i * 3;
			if (!!key && data.display_id.search(key) === 0) {
				colors[baseId + 0] = 0.0;
				colors[baseId + 1] = 1.0;
				colors[baseId + 2] = 1.0;
				if (data.search_id === key) {
					ret = data;
				}
			} else {
				colors[baseId + 0] = colors[baseId + 1] = colors[baseId + 2] = 1.0;
			}
		});
		this.particle.geometry.addAttribute('color', new THREE.BufferAttribute(colors, 3));
		return ret;
	}
	resize(width, height) {
		this.width = width;
		this.height = height;
		this.calculateGeometryPositions();
	}
};