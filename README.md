# Photon Sphere Studio 🌌

**3D Black Hole Visualization with Warped Spacetime Grid**

An interactive 3D visualization demonstrating photon geodesics (light ray paths) around a Schwarzschild black hole, featuring a dramatically warped spacetime grid and real-time animation controls.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.7+-orange.svg)

---

## 📸 Visualization Preview

### 3D Warped Spacetime Funnel
![3D Spacetime Grid Animation](photon_sphere_3d_full.gif)

*Interactive 3D funnel-shaped grid showing extreme spacetime curvature around a black hole. The grid warps dramatically inward near the event horizon, demonstrating how gravity curves spacetime itself.*

### 2D Light Bending Animation
![2D Light Bending](light_bending_lensing.gif)

*Side-by-side comparison of straight light paths (flat spacetime) versus curved light paths (around black hole), featuring a lensed accretion disk.*

---

## ✨ Features

### 🎨 Realistic Physics Visualization
- **Funnel-Shaped Spacetime Grid**: 3D grid that warps dramatically toward the black hole center
- **Extreme Gravitational Curvature**: Schwarzschild-inspired warping showing black hole's intense gravity
- **Photon Geodesics**: Accurate light ray paths calculated using general relativity equations
- **Gravitational Lensing**: Shows how light from background objects bends around the black hole
- **Event Horizon**: Visual representation of the point of no return

### 🎮 Interactive Controls
- **Rotation Slider**: Rotate view 360° around the black hole
- **Tilt Slider**: Adjust elevation from -90° to 90°
- **Zoom Slider**: Zoom in for details or out for full view (0.5x - 2.0x)
- **Play/Pause Buttons**: Control photon animation
- **Auto-Rotate Toggle**: Enable automatic camera rotation

### 🌈 Color-Coded Physics
- 🔴 **Red Grid Lines**: Near event horizon - extreme curvature
- 🟠 **Orange Grid Lines**: Moderate distance - strong warping
- 🟡 **Yellow Grid Lines**: Medium distance - visible curvature
- 🔵 **Blue Grid Lines**: Far from black hole - minimal warping
- 🟡 **Yellow Photon Rays**: Light rays that escape the black hole
- 🔴 **Red Photon Rays**: Light rays captured by the black hole

### 💾 Export Options
- **Animated GIF Output**: Automatically saves animations (no ffmpeg required!)
- **High-Resolution Rendering**: Configurable DPI for publication-quality output

---

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install numpy matplotlib scipy pillow
```

---

## 💻 Usage

### Running the 3D Visualization

```bash
python Photon_Sphere_3D.py
```

**Features:**
- 3D warped spacetime funnel grid
- Extreme gravitational curvature visualization
- Interactive camera controls (rotate, tilt, zoom)
- Photon geodesic animation
- Saves as `photon_sphere_3d_full.gif`

### Running the 2D Light Bending Visualization

```bash
python Photon_Sphere_Studio.py
```

**Features:**
- 2D comparison of flat vs curved light paths
- Lensed accretion disk
- Multiple impact parameter rays
- Saves as `light_bending_lensing.gif`

---

## 🎯 Interactive Controls Guide

### 3D Visualization Controls

Once the 3D visualization window opens:

1. **Camera Controls** (Bottom sliders):
   - **Rotate (Azimuth)**: 0° - 360° horizontal rotation
   - **Tilt (Elevation)**: -90° to 90° vertical angle
   - **Zoom**: 0.5x (far) to 2.0x (close-up)

2. **Animation Controls** (Buttons):
   - **▶ Play**: Start photon trajectory animation
   - **⏸ Pause**: Pause animation
   - **Auto-Rotate**: Toggle automatic 360° camera rotation

3. **Mouse Interaction**:
   - Matplotlib's native 3D rotation (click and drag)
   - Works in combination with sliders

---

## 🔬 Physics & Mathematics

### Spacetime Warping

The visualization uses a **Schwarzschild-inspired warping function** to demonstrate how black holes curve spacetime:

```python
warp_depth = -6.0 × √(rs / r) × (1 - r/r_max)^0.3
```

Where:
- `rs` = Schwarzschild radius (event horizon)
- `r` = radial distance from black hole center
- `r_max` = maximum grid extent

This creates an **extreme gravity well funnel** effect, showing that black holes create much stronger spacetime curvature than planets or stars.

### Schwarzschild Metric

The **Schwarzschild metric** describes spacetime around a non-rotating black hole:

```
ds² = -(1 - rs/r)c²dt² + (1 - rs/r)⁻¹dr² + r²dΩ²
```

**Event horizon** is located at:
```
rs = 2GM/c²
```

Where:
- `G` = gravitational constant
- `M` = black hole mass
- `c` = speed of light

### Photon Geodesics

Light rays follow **geodesic equations** in curved spacetime. The program numerically integrates:

```
d²u/dφ² + u = 3Mu²
```

Where `u = 1/r` and `φ` is the angular coordinate. This is solved using the **Runge-Kutta 4th order method** (`scipy.integrate.solve_ivp`).

**Impact Parameter**: Determines the trajectory:
- **Large b** (b > 3M): Light deflects but escapes
- **Small b** (b < 3M): Light captured or orbits
- **b = 3M**: Photon sphere (unstable circular orbit)

---

## 📊 Technical Details

### Key Components

#### `Photon_Sphere_3D.py` - 3D Visualization
- **Warped Grid Generation**: Creates funnel-shaped Cartesian grid
- **Schwarzschild Warping**: Applies extreme curvature transformation
- **3D Photon Trajectories**: Calculates geodesics in 3D space
- **Interactive Controls**: Sliders, buttons, and matplotlib integration
- **Animation Export**: PillowWriter for GIF output

#### `Photon_Sphere_Studio.py` - 2D Visualization  
- **2D Geodesic Integration**: Simplified polar coordinate system
- **Flat Space Comparison**: Shows undeflected light paths
- **Accretion Disk Lensing**: Weak-field gravitational lensing approximation
- **Multi-Ray Rendering**: Multiple impact parameters simultaneously

### Technologies Used

- **NumPy**: Numerical computations and array operations
- **Matplotlib**: 3D plotting, animation, and interactive widgets
- **SciPy**: Differential equation solving (ODE integration)
- **Pillow**: GIF animation export (no ffmpeg dependency!)

---

## 🎓 Educational Value

This visualization is ideal for:

- **Teaching General Relativity**: Visual demonstration of spacetime curvature
- **Understanding Black Holes**: See how extreme gravity warps space
- **Learning Differential Geometry**: Geodesics in curved spacetime
- **Studying Astrophysics**: Gravitational lensing and photon capture
- **Research Presentations**: High-quality, publication-ready visualizations

### Key Concepts Demonstrated

1. **Spacetime Curvature**: Grid visibly warps near massive objects
2. **Event Horizon**: The point of no return for light
3. **Photon Sphere**: Unstable orbit at r = 3M
4. **Gravitational Lensing**: Light bending around massive objects
5. **Geodesics**: "Straight" paths in curved spacetime

---

## 🎨 Visual Design

The visualization employs professional scientific visualization techniques:

- **Color Mapping**: Distance-based gradient (red → orange → yellow → blue)
- **Transparency Layers**: Alpha blending for depth perception
- **Smooth Curves**: Anti-aliased rendering for visual quality
- **Clean Background**: White background for publication quality
- **Dynamic Lighting**: Shaded surfaces on 3D objects
- **Grid Hierarchy**: Multiple line weights for visual clarity

---

## 🤝 Contributing

Contributions are welcome! Areas for enhancement:

- **Kerr Metric**: Add rotating black hole spacetime
- **Multiple Black Holes**: Binary black hole systems
- **Ergosphere**: Visualization for rotating black holes
- **Ray Tracing**: Full raytraced rendering
- **VR Support**: Virtual reality interface
- **Real Data**: Integration with actual black hole observations

Feel free to:
- Report bugs via GitHub Issues
- Suggest new features
- Submit pull requests
- Improve documentation

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Albert Einstein**: General Theory of Relativity (1915)
- **Karl Schwarzschild**: Schwarzschild solution (1916)
- **Event Horizon Telescope**: First black hole image (M87*, 2019)
- **Matplotlib Development Team**: Excellent 3D visualization tools
- **SciPy Contributors**: Robust numerical integration methods

---

## 📧 Contact & Support

- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions
- **Documentation**: See code docstrings for implementation details

---

## 🌟 Gallery

### Photon Trajectories
The yellow and red rays show how light bends around the black hole:
- **Yellow rays**: Deflected but escape to infinity
- **Red rays**: Captured by the black hole's gravity

### Spacetime Grid
The funnel-shaped grid demonstrates:
- Space itself is curved by mass
- Stronger curvature closer to the event horizon
- Black holes create extreme warping (much more than stars)

---

**Explore the fascinating physics of black holes and general relativity! 🌌✨**

*"Spacetime tells matter how to move; matter tells spacetime how to curve."* - John Archibald Wheeler
