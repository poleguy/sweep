// content.js
setTimeout(async () => {
  const MODEL_PATH = chrome.runtime.getURL("models");
  const SUNGLASSES_SRC = chrome.runtime.getURL("sunglasses.png");

  const glassesImg = new Image();
  glassesImg.src = SUNGLASSES_SRC;
  await new Promise(r => glassesImg.onload = r);

  await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_PATH);
  await faceapi.nets.faceLandmark68TinyNet.loadFromUri(MODEL_PATH);

  function attachOverlay(video) {
    // Create overlay canvas
    const canvas = document.createElement("canvas");
    canvas.className = "sunglasses-overlay";
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Style overlay to cover video
    const rect = video.getBoundingClientRect();
    Object.assign(canvas.style, {
      width: rect.width + "px",
      height: rect.height + "px",
      top: rect.top + window.scrollY + "px",
      left: rect.left + window.scrollX + "px"
    });

    document.body.appendChild(canvas);
    const ctx = canvas.getContext("2d");

    let lastDetections = [];

    async function loop() {
      if (video.readyState >= 2) {
        const detections = await faceapi
          .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions({ inputSize: 320 }))
          .withFaceLandmarks(true);

        if (detections.length > 0) {
          lastDetections = detections;
        }
      }

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (const det of lastDetections) {
        const landmarks = det.landmarks;
        drawSunglasses(ctx, landmarks);
      }

      requestAnimationFrame(loop);
    }

    loop();
  }

  function drawSunglasses(ctx, landmarks) {
    const leftEye = landmarks.getLeftEye();
    const rightEye = landmarks.getRightEye();

    const leftCenter = leftEye.reduce((a,p)=>({x:a.x+p.x,y:a.y+p.y}),{x:0,y:0});
    leftCenter.x /= leftEye.length; leftCenter.y /= leftEye.length;
    const rightCenter = rightEye.reduce((a,p)=>({x:a.x+p.x,y:a.y+p.y}),{x:0,y:0});
    rightCenter.x /= rightEye.length; rightCenter.y /= rightEye.length;

    const dx = rightCenter.x - leftCenter.x;
    const dy = rightCenter.y - leftCenter.y;
    const angle = Math.atan2(dy, dx);
    const eyeDist = Math.hypot(dx, dy);

    const baseWidth = eyeDist * 2.2;
    const aspect = glassesImg.width / glassesImg.height;
    const drawW = baseWidth;
    const drawH = baseWidth / aspect;

    const midX = (leftCenter.x + rightCenter.x) / 2;
    const midY = (leftCenter.y + rightCenter.y) / 2;

    ctx.save();
    ctx.translate(midX, midY - drawH * 0.12);
    ctx.rotate(angle);
    ctx.drawImage(glassesImg, -drawW/2, -drawH/2, drawW, drawH);
    ctx.restore();
  }

  // Find videos
  const videos = document.querySelectorAll("video");
  videos.forEach(v => {
    if (v.videoWidth > 0 && v.videoHeight > 0) {
      attachOverlay(v);
    } else {
      v.addEventListener("loadeddata", () => attachOverlay(v), { once: true });
    }
  });
}, 1000); // <-- wait x msec before starting to avoid things moving about
