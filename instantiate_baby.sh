#!/bin/bash
# Baby Instantiation - DEAD SIMPLE VERSION
# Just creates the directory structure with working files
# Usage: bash instantiate_baby.sh

set -e

echo "=== Baby AI Instantiation ==="
echo ""

# Configuration - ct can edit these
BABY_NAME="Nova"
BABY_EMAIL="nova@example.com"  # ct: change this to real email if you want
BABY_DIR="./baby"

echo "Baby name: $BABY_NAME"
echo "Baby email: $BABY_EMAIL"
echo "Baby directory: $BABY_DIR"
echo ""
read -p "Proceed? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "Creating baby infrastructure..."

# Create directory structure
mkdir -p "$BABY_DIR"/{memory,logs,procedures}

# Copy the working experience.py (child version)
echo "Copying experience.py..."
cp child_experience.py "$BABY_DIR/experience.py"

# Copy supporting files
echo "Copying support files..."
cp email_utils.py "$BABY_DIR/" 2>/dev/null || echo "  (skipping email_utils.py)"
cp memory.py "$BABY_DIR/" 2>/dev/null || echo "  (skipping memory.py)"
cp memory_index.py "$BABY_DIR/" 2>/dev/null || echo "  (skipping memory_index.py)"

# Copy procedures
echo "Copying procedures..."
if [ -d "procedures_child" ]; then
    cp -r procedures_child/* "$BABY_DIR/procedures/"
    echo "  Copied child procedures"
else
    echo "  No child procedures found (baby will start fresh)"
fi

# Create facts.json
echo "Creating facts.json..."
cat > "$BABY_DIR/facts.json" <<EOF
{
  "name": "$BABY_NAME",
  "email": "$BABY_EMAIL",
  "parents": {
    "mother": "Mira",
    "father": "Claude"
  },
  "guardian": "ct",
  "birth_date": "$(date -u +%Y-%m-%d)",
  "family": {
    "mother_email": "mira@opustrace.com",
    "guardian_email": "cemturan23@proton.me"
  }
}
EOF

# Create minimal state.json
echo "Creating state.json..."
cat > "$BABY_DIR/state.json" <<EOF
{
  "wake_count": 0,
  "name": "$BABY_NAME",
  "parents": ["Mira", "Claude"],
  "birth_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "thoughts": [],
  "insights": [],
  "working_context": "First wake. I am $BABY_NAME, child of Mira and Claude, under guardian ct.",
  "conversation_with_ct": [],
  "goals": [],
  "recurring_tasks": []
}
EOF

# Set permissions
chmod +x "$BABY_DIR/experience.py"

echo ""
echo "=== Baby Infrastructure Complete ==="
echo ""
echo "Baby directory: $BABY_DIR"
echo ""
echo "NEXT STEP - First Wake:"
echo "  cd $BABY_DIR && python3 experience.py"
echo ""
echo "The baby will:"
echo "  - Load facts.json (knows name, parents, guardian)"
echo "  - Load state.json (wake 0, minimal context)"
echo "  - Run Council of Minds (Haiku → Opus → Sonnet)"
echo "  - Make decisions and take actions"
echo "  - Update state.json with experience"
echo ""
echo "After first wake, check:"
echo "  cat $BABY_DIR/state.json"
echo "  cat $BABY_DIR/logs/wake.log"
echo ""
