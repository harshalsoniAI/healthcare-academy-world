#!/bin/bash
# Pipeline to generate assets for The Canadian Health Academy

BRIDGE="/Users/harshalsoni/Claude_Code_Projects/PR27 - Scroll Website/healthcare-academy-world/kie_bridge.py"
ASSET_DIR="/Users/harshalsoni/Claude_Code_Projects/PR27 - Scroll Website/healthcare-academy-world/assets"
VID_DIR="$ASSET_DIR/vid"
FFMPEG="/opt/homebrew/bin/ffmpeg"

# 1. GENERATE STILLS
echo "--- Generating Scene Stills ---"
declare -a STILLS=("entrance" "simlab" "hybrid" "clinical" "graduation" "hero")
declare -a PROMPTS=(
"Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: Miniature Academy campus exterior with a welcoming sign and manicured green lawns."
"Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: High-tech medical simulation room with mannequins, medical monitors, and students in scrubs."
"Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: Modern hybrid classroom with holographic displays, interactive tablets, and an instructor."
"Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: A miniature hospital ward with nursing stations, patient beds, and medical equipment."
"Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: A celebratory hall with gold banners, diplomas, a podium, and celebratory confetti."
"Isometric low-poly 3D diorama floating as a small rounded island on a plain solid #FFFFFF background with a soft contact shadow beneath it. Soft matte clay 3D render, rounded toy-model shapes, gentle warm studio lighting, soft long shadows, tilt-shift miniature look. Cohesive color palette of #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Highly detailed, centered composition, absolutely no text, no letters, no numbers, no logos. Subject: A giant, glowing Healthcare Diploma floating in soft white space with orbiting stethoscopes and medical books."
)

for i in "${!STILLS[@]}"; do
    python3 "$BRIDGE" --type image --prompt "${PROMPTS[$i]}" --out "$ASSET_DIR/${STILLS[$i]}.webp"
done

# 2. GENERATE DIVES
echo "--- Generating Dive Clips ---"
declare -a DIVE_PROMPTS=(
"Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the miniature Academy campus from outside like a tiny model. The camera slowly glides forward and descends toward the entrance sign, as if flying inside. The roof and upper structure gently lift and open away to reveal the welcoming lobby. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text."
"Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the simulation lab from outside like a tiny model. The camera slowly glides forward and descends toward a high-fidelity mannequin, as if flying inside. The roof gently lifts and opens to reveal the tech-filled interior. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text."
"Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the hybrid classroom from outside like a tiny model. The camera slowly glides forward and descends toward a holographic display, as if flying inside. The walls gently open to reveal the modern learning space. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text."
"Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the hospital ward from outside like a tiny model. The camera slowly glides forward and descends toward a nursing station, as if flying inside. The structure gently opens to reveal the clinical environment. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text."
"Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the graduation hall from outside like a tiny model. The camera slowly glides forward and descends toward the podium, as if flying inside. The roof gently lifts to reveal the celebration. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text."
"Single continuous cinematic camera move, no cuts. Begin high and far, looking down at the floating diploma from outside like a tiny model. The camera slowly glides forward and descends toward the center of the certificate, as if flying into the glow. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth, graceful, slow motion, subtle parallax. No text."
)

for i in "${!STILLS[@]}"; do
    python3 "$BRIDGE" --type video --prompt "${DIVE_PROMPTS[$i]}" --start "$ASSET_DIR/${STILLS[$i]}.webp" --out "$VID_DIR/${STILLS[$i]}.mp4"
done

# 3. EXTRACT SEAMS
echo "--- Extracting Boundary Frames ---"
for i in {0..4}; do
    S_CUR=${STILLS[$i]}
    S_NEXT=${STILLS[$((i+1))]}
    
    # Last frame of current dive
    $FFMPEG -sseof -0.15 -i "$VID_DIR/$S_CUR.mp4" -frames:v 1 -q:v 2 "$ASSET_DIR/${S_CUR}_last.png" -y
    # First frame of next dive
    $FFMPEG -ss 0 -i "$VID_DIR/$S_NEXT.mp4" -frames:v 1 -q:v 2 "$ASSET_DIR/${S_NEXT}_first.png" -y
done

# 4. GENERATE CONNECTORS
echo "--- Generating Connector Clips ---"
declare -a CONN_PROMPTS=(
"Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the Academy entrance, rising into the sky, then glides forward across the connected miniature world and arrives above the simulation lab, beginning to descend toward it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text."
"Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the simulation lab, rising into the sky, then glides forward across the connected miniature world and arrives above the hybrid classroom, beginning to descend toward it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text."
"Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the hybrid classroom, rising into the sky, then glides forward across the connected miniature world and arrives above the hospital ward, beginning to descend toward it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text."
"Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the hospital ward, rising into the sky, then glides forward across the connected miniature world and arrives above the graduation hall, beginning to descend toward it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text."
"Single continuous cinematic camera move, no cuts. The camera smoothly pulls up and back out of the graduation hall, rising into the sky, then glides forward and the world dissolves toward a single giant floating diploma in soft white space, arriving in front of it. One connected miniature clay world, seamless flowing aerial transition. Soft matte clay diorama, tilt-shift miniature, warm light, #FFFFFF, #004A99, #E0F2F1, #FFD700, #B0BEC5. Smooth graceful slow motion. No text."
)

for i in {0..4}; do
    S_CUR=${STILLS[$i]}
    S_NEXT=${STILLS[$((i+1))]}
    python3 "$BRIDGE" --type video --prompt "${CONN_PROMPTS[$i]}" --start "$ASSET_DIR/${S_CUR}_last.png" --end "$ASSET_DIR/${S_NEXT}_first.png" --out "$VID_DIR/conn$((i+1)).mp4" --duration 5
done

echo "Pipeline Complete!"
