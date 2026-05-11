const fs = require('fs');
const path = require('path');

const rootDir = __dirname;
const outputFile = path.join(rootDir, 'projects_data.js');

// Helper to find all index.html files
function findIndexFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    // Ignore node_modules, .git, and the root directory's own index.html
    if (file === 'node_modules' || file === '.git') return;
    
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      findIndexFiles(filePath, fileList);
    } else {
      if (file === 'index.html' && dir !== rootDir) {
        fileList.push(filePath);
      }
    }
  });

  return fileList;
}

// Generate project metadata
function generateProjectsData() {
  console.log('Scanning directories for projects...');
  const indexFiles = findIndexFiles(rootDir);
  
  const projects = indexFiles.map(filePath => {
    // Make path relative to root
    const relativePath = path.relative(rootDir, filePath);
    const parts = relativePath.split(path.sep);
    
    // Determine category and name
    let category = 'Uncategorized';
    let name = 'Unknown Project';
    
    if (parts.length >= 2) {
      category = parts[0];
      // Try to format category name beautifully
      category = category.replace(/[-_]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      
      if (parts.length === 2) {
         name = category; 
      } else {
         name = parts[parts.length - 2];
         name = name.replace(/[-_]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      }
    }

    return {
      name,
      category,
      url: `./${relativePath.replace(/\\/g, '/')}`,
      image: `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&color=fff&size=512` // Fallback image placeholder
    };
  });

  const fileContent = `// Auto-generated file. Run node update_projects.js to update.
const projectsData = ${JSON.stringify(projects, null, 2)};
`;

  fs.writeFileSync(outputFile, fileContent, 'utf-8');
  console.log(`Successfully generated projects_data.js with ${projects.length} projects!`);
}

generateProjectsData();
