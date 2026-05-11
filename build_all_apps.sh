#!/bin/bash
echo "Starting Mass Build of Node.js Templates..."

find /home/angish/project -maxdepth 3 -name package.json | while read pkg; do
    dir=$(dirname "$pkg")
    
    # Skip the main portfolios so we don't accidentally break them
    if [[ "$dir" == *Sayanth-portfolio* ]] || [[ "$dir" == *my-portfolio-website* ]] || [[ "$dir" == *node_modules* ]]; then
        continue
    fi
    
    echo "======================================"
    echo "Processing: $dir"
    echo "======================================"
    
    cd "$dir" || continue
    
    # Attempt to install dependencies. Using legacy-peer-deps since many of these are older templates
    npm install --legacy-peer-deps --no-fund --no-audit || echo "Failed to install dependencies in $dir"
    
    # Attempt to build
    npm run build || echo "Failed to build $dir"
done

echo "Mass build complete!"
