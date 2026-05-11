const fs = require('fs');
const path = require('path');

const rootDir = '/home/angish/project';
const outputFile = path.join(rootDir, '3d-websites', 'Sayanth-portfolio', 'src', 'data', 'projectsData.json');

function findIndexFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);

  const hasPackageJson = files.includes('package.json');
  const isIgnoredRoot = dir.includes('Sayanth-portfolio') || dir.includes('my-portfolio-website') || dir.includes('node_modules') || dir.includes('.git');

  // If it's a Node project (and not our main portfolio), try to find its compiled build index.html
  if (!isIgnoredRoot && hasPackageJson) {
      const possibleBuilds = ['dist', 'build', 'out'];
      let foundBuild = false;
      for (const buildDir of possibleBuilds) {
          const buildPath = path.join(dir, buildDir, 'index.html');
          if (fs.existsSync(buildPath)) {
              fileList.push(buildPath);
              foundBuild = true;
          }
      }
      // If we found a compiled build, we stop traversing this project to avoid duplicate raw public/index.html files
      if (foundBuild) return fileList;
      
      // If we didn't find a build, we still shouldn't link to raw public/index.html because it won't work statically anyway.
      // So we return early for Node projects unless we specifically want to try parsing their public folders. 
      // Let's just return to keep the gallery clean of broken apps.
      return fileList;
  }

  files.forEach(file => {
    if (['node_modules', '.git', '.gemini', '3d-websites', 'documentation', 'docs', 'vendor', 'src'].includes(file)) return;
    
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

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateProjectsData() {
  let indexFiles = findIndexFiles(rootDir);
  
  indexFiles = indexFiles.sort(() => 0.5 - Math.random());
  
  const tierCounts = { S: 2, A: 11, B: 44, C: 175 };
  
  const projects = indexFiles.map((filePath, index) => {
    const relativePath = path.relative(rootDir, filePath);
    const parts = relativePath.split(path.sep);
    
    let category = 'Uncategorized';
    let name = 'Unknown Project';
    
    if (parts.length >= 2) {
      category = parts[0].replace(/[-_]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      
      if (parts.length === 2) {
         name = category; 
      } else {
         let namePart = parts[parts.length - 2];
         // Don't name a project "Dist" or "Build" if we're linking to its compiled folder
         if (['dist', 'build', 'out'].includes(namePart.toLowerCase()) && parts.length > 2) {
             namePart = parts[parts.length - 3];
         }
         name = namePart.replace(/[-_]/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
      }
    }

    let tier = 'D';
    let price = 0;

    if (tierCounts.S > 0) {
        tier = 'S';
        price = getRandomInt(4000, 10000);
        tierCounts.S--;
    } else if (tierCounts.A > 0) {
        tier = 'A';
        price = getRandomInt(2000, 5000);
        tierCounts.A--;
    } else if (tierCounts.B > 0) {
        tier = 'B';
        price = getRandomInt(500, 2000);
        tierCounts.B--;
    } else if (tierCounts.C > 0) {
        tier = 'C';
        price = getRandomInt(100, 500);
        tierCounts.C--;
    } else {
        tier = 'D';
        price = getRandomInt(0, 100);
    }

    const image = `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&color=fff&size=512`;

    return {
      id: index + 1,
      name,
      category,
      price,
      tier,
      url: `http://localhost:8000/${relativePath.replace(/\\/g, '/')}`,
      image
    };
  });

  fs.writeFileSync(outputFile, JSON.stringify(projects, null, 2), 'utf-8');
  console.log(`Successfully generated projectsData.json with ${projects.length} projects!`);
}

generateProjectsData();
