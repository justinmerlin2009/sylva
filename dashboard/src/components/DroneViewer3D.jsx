/**
 * SYLVA-1 3D Drone Viewer Component
 *
 * Interactive Three.js viewer for the Sylva drone with sensor payload.
 * Supports rotation, zoom, and auto-rotation.
 *
 * Usage:
 *   <DroneViewer3D />
 *
 * To use with actual 3D model:
 * 1. Export drone from Blender as GLTF (.glb)
 * 2. Place in /public/models/sylva_drone.glb
 * 3. Set USE_PLACEHOLDER = false
 */

import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader';

// Set to false when you have the actual GLTF model
const USE_PLACEHOLDER = true;
const MODEL_PATH = '/models/sylva_drone.glb';

const DroneViewer3D = ({ width = '100%', height = '500px', autoRotate = true }) => {
  const containerRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0e14);

    // Get container dimensions
    const container = containerRef.current;
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;

    // Camera
    const camera = new THREE.PerspectiveCamera(
      45,
      containerWidth / containerHeight,
      0.1,
      1000
    );
    camera.position.set(3, 2, 3);
    camera.lookAt(0, 0, 0);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(containerWidth, containerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.autoRotate = autoRotate;
    controls.autoRotateSpeed = 1.0;
    controls.minDistance = 1.5;
    controls.maxDistance = 10;
    controls.target.set(0, 0, 0);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffffff, 1);
    keyLight.position.set(5, 5, 5);
    keyLight.castShadow = true;
    scene.add(keyLight);

    const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
    fillLight.position.set(-5, 3, -5);
    scene.add(fillLight);

    const rimLight = new THREE.DirectionalLight(0x51ab5a, 0.3);
    rimLight.position.set(0, -3, 5);
    scene.add(rimLight);

    // Materials
    const fuselageMaterial = new THREE.MeshStandardMaterial({
      color: 0xf0f0f0,
      metalness: 0.1,
      roughness: 0.4,
    });

    const wingMaterial = new THREE.MeshStandardMaterial({
      color: 0xe8e8e8,
      metalness: 0.1,
      roughness: 0.5,
    });

    const darkMaterial = new THREE.MeshStandardMaterial({
      color: 0x222222,
      metalness: 0.3,
      roughness: 0.3,
    });

    const payloadMaterial = new THREE.MeshStandardMaterial({
      color: 0x1a1a1a,
      metalness: 0.2,
      roughness: 0.4,
    });

    const greenMaterial = new THREE.MeshStandardMaterial({
      color: 0x51ab5a,
      metalness: 0.0,
      roughness: 0.4,
    });

    const lensMaterial = new THREE.MeshStandardMaterial({
      color: 0x0a1a2a,
      metalness: 0.5,
      roughness: 0.1,
    });

    const ledMaterial = new THREE.MeshStandardMaterial({
      color: 0x00ff00,
      emissive: 0x00ff00,
      emissiveIntensity: 2,
    });

    const nvidiaMaterial = new THREE.MeshStandardMaterial({
      color: 0x76b900,
      metalness: 0.0,
      roughness: 0.3,
    });

    let droneGroup;

    if (USE_PLACEHOLDER) {
      // Create placeholder drone geometry
      droneGroup = new THREE.Group();

      // Fuselage (elongated ellipsoid shape)
      const fuselageGeometry = new THREE.CapsuleGeometry(0.15, 0.8, 8, 16);
      const fuselage = new THREE.Mesh(fuselageGeometry, fuselageMaterial);
      fuselage.rotation.z = Math.PI / 2;
      fuselage.position.y = 0.05;
      fuselage.castShadow = true;
      droneGroup.add(fuselage);

      // Nose cone
      const noseGeometry = new THREE.SphereGeometry(0.12, 16, 16, 0, Math.PI);
      const nose = new THREE.Mesh(noseGeometry, fuselageMaterial);
      nose.rotation.z = -Math.PI / 2;
      nose.position.set(-0.55, 0.05, 0);
      nose.castShadow = true;
      droneGroup.add(nose);

      // Wings
      const wingShape = new THREE.Shape();
      wingShape.moveTo(0, 0);
      wingShape.lineTo(1.2, 0.1);
      wingShape.lineTo(1.3, 0);
      wingShape.lineTo(1.2, -0.05);
      wingShape.lineTo(0, -0.15);
      wingShape.lineTo(0, 0);

      const wingExtrudeSettings = {
        depth: 0.02,
        bevelEnabled: true,
        bevelThickness: 0.01,
        bevelSize: 0.01,
        bevelSegments: 2,
      };

      const wingGeometry = new THREE.ExtrudeGeometry(wingShape, wingExtrudeSettings);

      // Right wing
      const rightWing = new THREE.Mesh(wingGeometry, wingMaterial);
      rightWing.position.set(-0.1, 0.1, 0);
      rightWing.rotation.y = -Math.PI / 2;
      rightWing.castShadow = true;
      droneGroup.add(rightWing);

      // Left wing
      const leftWing = new THREE.Mesh(wingGeometry, wingMaterial);
      leftWing.position.set(-0.1, 0.1, 0);
      leftWing.rotation.y = Math.PI / 2;
      leftWing.scale.z = -1;
      leftWing.castShadow = true;
      droneGroup.add(leftWing);

      // V-Tail
      const tailShape = new THREE.Shape();
      tailShape.moveTo(0, 0);
      tailShape.lineTo(0.4, 0.3);
      tailShape.lineTo(0.45, 0.28);
      tailShape.lineTo(0.08, 0);
      tailShape.lineTo(0, 0);

      const tailGeometry = new THREE.ExtrudeGeometry(tailShape, {
        depth: 0.015,
        bevelEnabled: false,
      });

      // Right V-tail
      const rightTail = new THREE.Mesh(tailGeometry, wingMaterial);
      rightTail.position.set(0.35, 0.05, 0.02);
      rightTail.castShadow = true;
      droneGroup.add(rightTail);

      // Left V-tail
      const leftTail = new THREE.Mesh(tailGeometry, wingMaterial);
      leftTail.position.set(0.35, 0.05, -0.02);
      leftTail.scale.z = -1;
      leftTail.castShadow = true;
      droneGroup.add(leftTail);

      // Motors
      const motorGeometry = new THREE.CylinderGeometry(0.03, 0.03, 0.04, 16);

      const rightMotor = new THREE.Mesh(motorGeometry, darkMaterial);
      rightMotor.position.set(-0.2, 0.1, 0.4);
      rightMotor.rotation.x = Math.PI / 2;
      droneGroup.add(rightMotor);

      const leftMotor = new THREE.Mesh(motorGeometry, darkMaterial);
      leftMotor.position.set(-0.2, 0.1, -0.4);
      leftMotor.rotation.x = Math.PI / 2;
      droneGroup.add(leftMotor);

      // Propellers (spinning discs for visual effect)
      const propGeometry = new THREE.CircleGeometry(0.12, 32);
      const propMaterial = new THREE.MeshStandardMaterial({
        color: 0x333333,
        transparent: true,
        opacity: 0.3,
        side: THREE.DoubleSide,
      });

      const rightProp = new THREE.Mesh(propGeometry, propMaterial);
      rightProp.position.set(-0.25, 0.1, 0.4);
      rightProp.rotation.y = Math.PI / 2;
      droneGroup.add(rightProp);

      const leftProp = new THREE.Mesh(propGeometry, propMaterial);
      leftProp.position.set(-0.25, 0.1, -0.4);
      leftProp.rotation.y = Math.PI / 2;
      droneGroup.add(leftProp);

      // ========== SENSOR PAYLOAD ==========
      const payloadGroup = new THREE.Group();

      // Gimbal arm
      const gimbalArmGeometry = new THREE.CylinderGeometry(0.015, 0.015, 0.06, 8);
      const gimbalArm = new THREE.Mesh(gimbalArmGeometry, darkMaterial);
      gimbalArm.position.set(0, -0.08, 0);
      payloadGroup.add(gimbalArm);

      // Payload housing
      const housingGeometry = new THREE.BoxGeometry(0.18, 0.08, 0.1);
      const housing = new THREE.Mesh(housingGeometry, payloadMaterial);
      housing.position.set(0, -0.15, 0);
      housing.castShadow = true;
      payloadGroup.add(housing);

      // RGB Camera lens
      const rgbLensGeometry = new THREE.CylinderGeometry(0.025, 0.025, 0.015, 16);
      const rgbLens = new THREE.Mesh(rgbLensGeometry, lensMaterial);
      rgbLens.position.set(-0.04, -0.15, 0.055);
      rgbLens.rotation.x = Math.PI / 2;
      payloadGroup.add(rgbLens);

      // RGB lens inner
      const rgbInnerGeometry = new THREE.CylinderGeometry(0.018, 0.018, 0.02, 16);
      const rgbInner = new THREE.Mesh(rgbInnerGeometry, darkMaterial);
      rgbInner.position.set(-0.04, -0.15, 0.06);
      rgbInner.rotation.x = Math.PI / 2;
      payloadGroup.add(rgbInner);

      // Hyperspectral sensor
      const hyperGeometry = new THREE.BoxGeometry(0.05, 0.025, 0.015);
      const hyperSensor = new THREE.Mesh(hyperGeometry, lensMaterial);
      hyperSensor.position.set(0.03, -0.14, 0.055);
      payloadGroup.add(hyperSensor);

      // LiDAR
      const lidarGeometry = new THREE.CylinderGeometry(0.018, 0.018, 0.012, 16);
      const lidar = new THREE.Mesh(lidarGeometry, darkMaterial);
      lidar.position.set(0.03, -0.16, 0.055);
      lidar.rotation.x = Math.PI / 2;
      payloadGroup.add(lidar);

      // LiDAR emitters (red dots)
      const emitterGeometry = new THREE.SphereGeometry(0.003, 8, 8);
      const emitterMaterial = new THREE.MeshStandardMaterial({
        color: 0xff3300,
        emissive: 0xff3300,
        emissiveIntensity: 1,
      });

      [-0.008, 0, 0.008].forEach((offset) => {
        const emitter = new THREE.Mesh(emitterGeometry, emitterMaterial);
        emitter.position.set(0.03 + offset, -0.16, 0.062);
        payloadGroup.add(emitter);
      });

      // Status LED
      const ledGeometry = new THREE.SphereGeometry(0.006, 8, 8);
      const led = new THREE.Mesh(ledGeometry, ledMaterial);
      led.position.set(-0.07, -0.13, 0.05);
      payloadGroup.add(led);

      // NVIDIA badge
      const badgeGeometry = new THREE.BoxGeometry(0.035, 0.012, 0.002);
      const badge = new THREE.Mesh(badgeGeometry, nvidiaMaterial);
      badge.position.set(0.055, -0.13, 0.051);
      payloadGroup.add(badge);

      // SYLVA text (simplified as green stripe)
      const sylvaGeometry = new THREE.BoxGeometry(0.06, 0.008, 0.002);
      const sylva = new THREE.Mesh(sylvaGeometry, greenMaterial);
      sylva.position.set(-0.01, -0.12, 0.051);
      payloadGroup.add(sylva);

      payloadGroup.position.set(-0.05, 0, 0);
      droneGroup.add(payloadGroup);

      // Position entire drone
      droneGroup.position.y = 0.2;
      scene.add(droneGroup);

      setLoading(false);
    } else {
      // Load actual GLTF model
      const loader = new GLTFLoader();
      loader.load(
        MODEL_PATH,
        (gltf) => {
          droneGroup = gltf.scene;
          droneGroup.traverse((child) => {
            if (child.isMesh) {
              child.castShadow = true;
              child.receiveShadow = true;
            }
          });
          scene.add(droneGroup);
          setLoading(false);
        },
        (progress) => {
          console.log('Loading progress:', (progress.loaded / progress.total) * 100, '%');
        },
        (err) => {
          console.error('Error loading model:', err);
          setError('Failed to load 3D model');
          setLoading(false);
        }
      );
    }

    // Ground plane (subtle)
    const groundGeometry = new THREE.CircleGeometry(5, 32);
    const groundMaterial = new THREE.MeshStandardMaterial({
      color: 0x0d1117,
      roughness: 0.9,
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.3;
    ground.receiveShadow = true;
    scene.add(ground);

    // Grid helper (subtle)
    const gridHelper = new THREE.GridHelper(4, 20, 0x1a1a1a, 0x1a1a1a);
    gridHelper.position.y = -0.29;
    scene.add(gridHelper);

    // Animation loop
    let animationId;
    const animate = () => {
      animationId = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // Handle resize
    const handleResize = () => {
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight;
      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationId);
      renderer.dispose();
      container.removeChild(renderer.domElement);
    };
  }, [autoRotate]);

  return (
    <div
      ref={containerRef}
      style={{
        width,
        height,
        position: 'relative',
        borderRadius: '8px',
        overflow: 'hidden',
      }}
    >
      {loading && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            color: '#51ab5a',
            fontSize: '14px',
          }}
        >
          Loading 3D model...
        </div>
      )}
      {error && (
        <div
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            color: '#ff4444',
            fontSize: '14px',
          }}
        >
          {error}
        </div>
      )}
      <div
        style={{
          position: 'absolute',
          bottom: '10px',
          left: '10px',
          color: '#666',
          fontSize: '11px',
        }}
      >
        Drag to rotate • Scroll to zoom
      </div>
    </div>
  );
};

export default DroneViewer3D;
