import os
import subprocess
import sys
from kie_bridge import generate_image, generate_video, download_file

# --- CONFIGURATION ---
ASSET_DIR = "assets"
VID_DIR = os.path.join(ASSET_DIR, "vid")
FFMPEG = "/opt/homebrew/bin/ffmpeg"

SCENES = [
    {"id": "entrance", "label": "Entrance", "prompt": "Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: Miniature Academy campus exterior with a welcoming sign and manicured green lawns."},
    {"id": "simlab", "label": "Sim Lab", "prompt": "Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: High-tech medical simulation room with mannequins, medical monitors, and students in scrubs."},
    {"id": "hybrid", "label": "Learning", "prompt": "Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: Modern hybrid classroom with holographic displays, interactive tablets, and an instructor."},
    {"id": "clinical", "label": "Clinical", "prompt": "Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: A miniature hospital ward with nursing stations, patient beds, and medical equipment."},
    {"id": "graduation", "label": "Graduation", "prompt": "Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: A celebratory hall with gold banners, diplomas, a podium, and celebratory confetti."},
    {"id": "hero", "label": "Enroll", "prompt": "Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: A giant, glowing Healthcare Diploma floating in soft white space with orbiting stethoscopes and medical books."},
]

DIVE_PROMPTS = [
    "Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the miniature Academy campus from outside like a tiny model. The camera slowly glides forward and descends toward the entrance sign, as if flying inside. The roof and upper structure gently lift and open away to reveal the welcoming lobby. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text.",
    "Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the simulation lab from outside like a tiny model. The camera slowly glides forward and descends toward a high-fidelity mannequin, as if flying inside. The roof gently lifts and opens to reveal the tech-filled interior. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text.",
    "Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the hybrid classroom from outside like a tiny model. The camera slowly glides forward and descends toward a holographic display, as if flying inside. The walls gently open to reveal the modern learning space. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text.",
    "Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the hospital ward from outside like a tiny model. The camera slowly glides forward and descends toward a nursing station, as if flying inside. The structure gently opens to reveal the clinical environment. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text.",
    "Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the graduation hall from outside like a tiny model. The camera slowly glides forward and descends toward the podium, as if flying inside. The roof gently lifts to reveal the celebration. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text.",
    "Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the floating diploma from outside like a tiny model. The camera slowly glides forward and descends toward the center of the certificate, as if flying into the glow. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text.",
]

CONN_PROMPTS = [
    "Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the Academy entrance, rising into the sky, then glides forward across the connected miniature world and arrives above the simulation lab, beginning to descend toward it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text.",
    "Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the simulation lab, rising into the sky, then glides forward across the connected miniature world and arrives above the hybrid classroom, beginning to descend toward it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text.",
    "Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the hybrid classroom, rising into the sky, then glides forward across the connected miniature world and arrives above the hospital ward, beginning to descend toward it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text.",
    "Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the hospital ward, rising into the sky, then glides forward across the connected miniature world and arrives above the graduation hall, beginning to descend toward it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text.",
    "Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the graduation hall, rising into the sky, then glides forward and the world dissolves toward a single giant floating diploma in soft white space, arriving in front of it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text.",
]

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def run():
    ensure_dir(ASSET_DIR)
    ensure_dir(VID_DIR)

    # STEP 1: STILLS
    print("\n--- Step 1: Generating Scene Stills ---")
    for scene in SCENES:
        out_path = os.path.join(ASSET_DIR, f"{scene['id']}.webp")
        if os.path.exists(out_path):
            print(f"✅ {scene['id']} still exists. Skipping.")
            continue
        
        url = generate_image(scene['prompt'])
        if url:
            download_file(url, out_path)
            print(f"✅ Generated {scene['id']} still.")
        else:
            print(f"❌ FAILED to generate still for {scene['id']}. Stopping.")
            sys.exit(1)

    # STEP 2: DIVES
    print("\n--- Step 2: Generating Dive Clips ---")
    for i, scene in enumerate(SCENES):
        out_path = os.path.join(VID_DIR, f"{scene['id']}.mp4")
        start_img = os.path.join(ASSET_DIR, f"{scene['id']}.webp")
        
        if os.path.exists(out_path):
            print(f"✅ {scene['id']} dive exists. Skipping.")
            continue
        
        if not os.path.exists(start_img):
            print(f"❌ Missing start image for {scene['id']}. Stopping.")
            sys.exit(1)
            
        url = generate_video(DIVE_PROMPTS[i], start_image=start_img)
        if url:
            download_file(url, out_path)
            print(f"✅ Generated {scene['id']} dive.")
        else:
            print(f"❌ FAILED to generate dive for {scene['id']}. Stopping.")
            sys.exit(1)

    # STEP 3: EXTRACT BOUNDARIES
    print("\n--- Step 3: Extracting Boundary Frames ---")
    for i in range(len(SCENES) - 1):
        cur = SCENES[i]['id']
        nxt = SCENES[i+1]['id']
        
        last_frame = os.path.join(ASSET_DIR, f"{cur}_last.png")
        first_frame = os.path.join(ASSET_DIR, f"{nxt}_first.png")
        
        dive_cur = os.path.join(VID_DIR, f"{cur}.mp4")
        dive_nxt = os.path.join(VID_DIR, f"{nxt}.mp4")
        
        if not os.path.exists(dive_cur) or not os.path.exists(dive_nxt):
            print(f"❌ Missing videos for boundaries {cur} <-> {nxt}. Stopping.")
            sys.exit(1)
            
        # Extract last frame of cur
        subprocess.run([FFMPEG, "-sseof", "-0.15", "-i", dive_cur, "-frames:v", "1", "-q:v", "2", last_frame, "-y"], check=True)
        # Extract first frame of nxt
        subprocess.run([FFMPEG, "-ss", "0", "-i", dive_nxt, "-frames:v", "1", "-q:v", "2", first_frame, "-y"], check=True)
        print(f"✅ Extracted frames for {cur} <-> {nxt}.")

    # STEP 4: CONNECTORS
    print("\n--- Step 4: Generating Connector Clips ---")
    for i in range(len(SCENES) - 1):
        cur = SCENES[i]['id']
        nxt = SCENES[i+1]['id']
        out_path = os.path.join(VID_DIR, f"conn{i+1}.mp4")
        
        if os.path.exists(out_path):
            print(f"✅ Connector {i+1} exists. Skipping.")
            continue
            
        start_img = os.path.join(ASSET_DIR, f"{cur}_last.png")
        end_img = os.path.join(ASSET_DIR, f"{nxt}_first.png")
        
        if not os.path.exists(start_img) or not os.path.exists(end_img):
            print(f"❌ Missing boundary frames for connector {i+1}. Stopping.")
            sys.exit(1)
            
        url = generate_video(CONN_PROMPTS[i], start_image=start_img, end_image=end_img, duration=5)
        if url:
            download_file(url, out_path)
            print(f"✅ Generated connector {i+1}.")
        else:
            print(f"❌ FAILED to generate connector {i+1}. Stopping.")
            sys.exit(1)

    print("\n🎉 PIPELINE COMPLETE! Your world is ready.")

if __name__ == "__main__":
    run()
