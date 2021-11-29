const regions = [..."ABCDEFG"];
const connections = "AB AC BC BD CD CE CF DE EF";

const connectionMap = connections.split(" ").reduce((map, connection) => {
  let [a, b] = [...connection];
  map[a] = [...(map[a] || []), b];
  map[b] = [...(map[b] || []), a];

  return map;

}, {});

const regionColors = Object.fromEntries(regions.map(region => [region, "123"]));
const colorOptions = ["purple", "gold", "green"];
const solved = solve(regionColors);

function App() {
  const [w, setW] = React.useState(document.body.offsetWidth);
  const [h, setH] = React.useState(document.body.offsetHeight);

  const positions = [
    [.8*w*.2, .8*w*.5],
    [.8*w*.5, .8*w*.2],
    [.8*w*.55, .8*w*.5],
    [.8*w*.8, .8*w*.4],
    [.8*w*.8, .8*w*.6],
    [.8*w*.75, .8*w*.75],
    [.8*w*.775, .8*w*.875]
  ];  

  React.useEffect(
    () => {
      let eh = window.addEventListener("resize", function() {
        setW(document.body.offsetWidth);
        setH(document.body.offsetHeight);
      });

      return e => window.removeEventListener("resize", eh);
    }
  );

  const edges = connections.split(" ").map(c => {
    return c.split("").map(r => positions[regions.indexOf(r)]);
  });

  return <React.Fragment>
    {
      edges.map(([[x1, y1], [x2, y2]], i) => {
        return <line key={`line-${i}`} x1={x1} y1={y1} x2={x2} y2={y2} stroke="#4a4f5c" strokeWidth="6" strokeDasharray="5 5" />;
      })
    }
    {
      positions.map(([x, y], i) => {
        return <circle key={`circle-${i}`} cx={x} cy={y} r={w*0.03} className={colorOptions[solved[regions[i]]-1]} />;
      })
    }        
  </React.Fragment>;
}

function constrain(regionColors, region, color) {
  regionColors = {...regionColors};

  regionColors[region] = color;

  for (let otherNode of (connectionMap[region] || [])) {

    if (regionColors[otherNode].includes(color)) {
      regionColors[otherNode] = regionColors[otherNode].replace(color, "");

      switch (regionColors[otherNode].length) {
        case 1:
          return constrain(regionColors, otherNode, regionColors[otherNode]);
          break;
        case 0:
          throw new Error("Configuration invalid");
          break;

      }
    }
  }

  return regionColors;
}

function solve(regionColors) {
  for (let [region, colorOptions] of Object.entries(regionColors)) {
    if (colorOptions.length == 1) continue;

    for (let color of colorOptions) {
      try {
        let result = solve(constrain(regionColors, region, color));
        return result;
      } catch (e) { }
    }

    throw new Error("Unsatisfiable");
  }

  return regionColors;
}

ReactDOM.render(<App/>, document.querySelector("#nodes"));