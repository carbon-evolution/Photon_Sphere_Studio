# 3D Black Hole Visualization with TRUE 3D Warped Spacetime Grid
# Full 3D spherical grid showing spacetime curvature in all directions
# Features: 3D warped grid shells, animated light rays, interactive controls
# No ffmpeg required - saves as animated GIF using Pillow!

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.widgets import Slider, Button
import os

# ----------------------------
# CONFIG
# ----------------------------
SAVE_ANIMATION = True
ANIMATION_FILENAME = "photon_sphere_3d_full.gif"
FRAMES = 150
INTERVAL_MS = 50
DPI = 100

# Physical constants (geometric units)
M = 1.0
rs = 2.0 * M  # Schwarzschild radius
r_photon = 3.0 * M  # Photon sphere radius
PLOT_LIMIT = 15.0

# ----------------------------
# 3D Warped Spacetime Grid Functions - FUNNEL STYLE
# ----------------------------
def spacetime_warp_z(r, r_max=PLOT_LIMIT):
    """
    Calculate the Z-displacement (depth) due to spacetime warping.
    Creates the gravity well funnel effect.
    Black holes create extreme curvature.
    """
    if r <= rs:
        return -15  # Very deep well at event horizon
    
    # Strong Schwarzschild-inspired warping for black hole
    # Much steeper than for planets/stars
    warp_depth = -6.0 * np.sqrt(rs / r) * (1 - r/r_max)**0.3
    return warp_depth

def create_warped_cartesian_grid(grid_extent=PLOT_LIMIT, n_lines=24):
    """
    Create a funnel-shaped warped Cartesian grid.
    Returns lists of grid lines that warp downward near the black hole.
    """
    grid_lines = []
    
    # Create coordinate lines
    coords = np.linspace(-grid_extent, grid_extent, n_lines)
    
    # Grid lines parallel to X-axis (varying Y, constant X)
    for x_const in coords:
        y_line = np.linspace(-grid_extent, grid_extent, 100)
        x_line = np.ones_like(y_line) * x_const
        
        # Calculate radial distance and Z warping
        r_line = np.sqrt(x_line**2 + y_line**2)
        z_line = np.array([spacetime_warp_z(r) if r > 0 else spacetime_warp_z(0.01) for r in r_line])
        
        grid_lines.append((x_line, y_line, z_line))
    
    # Grid lines parallel to Y-axis (varying X, constant Y)
    for y_const in coords:
        x_line = np.linspace(-grid_extent, grid_extent, 100)
        y_line = np.ones_like(x_line) * y_const
        
        # Calculate radial distance and Z warping
        r_line = np.sqrt(x_line**2 + y_line**2)
        z_line = np.array([spacetime_warp_z(r) if r > 0 else spacetime_warp_z(0.01) for r in r_line])
        
        grid_lines.append((x_line, y_line, z_line))
    
    return grid_lines

def create_radial_grid_lines_funnel(n_radial=16, r_max=PLOT_LIMIT):
    """
    Create radial lines emanating from center down the funnel.
    """
    angles = np.linspace(0, 2*np.pi, n_radial, endpoint=False)
    radial_lines = []
    
    for angle in angles:
        r_vals = np.linspace(rs * 1.2, r_max, 50)
        x_line = r_vals * np.cos(angle)
        y_line = r_vals * np.sin(angle)
        z_line = np.array([spacetime_warp_z(r) for r in r_vals])
        
        radial_lines.append((x_line, y_line, z_line))
    
    return radial_lines

# ----------------------------
# Geodesic integrator for 3D null geodesics
# ----------------------------
def rk4_step(f, phi, y, h):
    k1 = f(phi, y)
    k2 = f(phi + 0.5*h, y + 0.5*h*k1)
    k3 = f(phi + 0.5*h, y + 0.5*h*k2)
    k4 = f(phi + h, y + h*k3)
    return y + (h/6.0)*(k1 + 2*k2 + 2*k3 + k4)

def geodesic_rhs(phi, y):
    u, up = y
    d2u = 3.0 * M * u**2 - u
    return np.array([up, d2u])

def integrate_ray_3d(b, theta_angle=0, phi_angle=0, phi_min=-4.0, phi_max=4.0, Nphi=1500):
    """
    Calculate a 3D light ray trajectory in any direction.
    theta_angle: initial polar angle
    phi_angle: initial azimuthal angle
    """
    phi_grid = np.linspace(phi_min, phi_max, Nphi)
    dphi = phi_grid[1] - phi_grid[0]
    y = np.zeros((Nphi, 2))
    y[0,0] = 1.0 / b
    y[0,1] = 0.0
    stop_i = Nphi
    
    for i in range(Nphi-1):
        y[i+1] = rk4_step(geodesic_rhs, phi_grid[i], y[i], dphi)
        if y[i+1,0] <= 0 or 1.0/y[i+1,0] < 1.01*rs:
            stop_i = i+2
            break
    
    u = y[:stop_i,0]
    r = 1.0 / u
    phi_vals = phi_grid[:stop_i]
    
    # Convert to 3D Cartesian coordinates with rotation
    x_2d = r * np.cos(phi_vals + phi_angle)
    y_2d = r * np.sin(phi_vals + phi_angle)
    
    # Rotate into 3D based on theta_angle
    x = x_2d * np.cos(theta_angle)
    y = y_2d
    z = x_2d * np.sin(theta_angle)
    
    return x, y, z, r

def create_straight_ray_3d(b, theta_angle, phi_angle, length=PLOT_LIMIT*2):
    """Create a straight light ray for comparison (flat spacetime)"""
    t = np.linspace(-length, length, 300)
    
    # Direction vector
    dir_x = np.cos(phi_angle) * np.cos(theta_angle)
    dir_y = np.sin(phi_angle)
    dir_z = np.cos(phi_angle) * np.sin(theta_angle)
    
    # Perpendicular offset for impact parameter b
    offset_x = -np.sin(phi_angle) * b
    offset_y = np.cos(phi_angle) * b
    offset_z = 0
    
    x = offset_x + t * dir_x
    y = offset_y + t * dir_y
    z = offset_z + t * dir_z
    
    return x, y, z

# ----------------------------
# Generate photon trajectories
# ----------------------------
print("Calculating photon trajectories...")

ray_configs = [
    # Escaping rays (yellow/golden) - larger impact parameter
    {'b': 10.0, 'theta': 0, 'phi': 0, 'color': '#FFD700', 'type': 'escape'},
    {'b': 9.0, 'theta': np.pi/6, 'phi': np.pi/4, 'color': '#FFA500', 'type': 'escape'},
    {'b': 8.5, 'theta': -np.pi/6, 'phi': np.pi/2, 'color': '#FFDB58', 'type': 'escape'},
    
    # Captured rays (red/pink) - smaller impact parameter
    {'b': 5.5, 'theta': np.pi/8, 'phi': -np.pi/6, 'color': '#FF1493', 'type': 'capture'},
    {'b': 5.0, 'theta': -np.pi/8, 'phi': 3*np.pi/4, 'color': '#FF69B4', 'type': 'capture'},
    {'b': 4.5, 'theta': np.pi/12, 'phi': np.pi, 'color': '#FF6B9D', 'type': 'capture'},
]

# Generate curved and straight rays
rays_3d = []
straight_rays_3d = []

for config in ray_configs:
    # Curved geodesic ray
    x, y, z, r = integrate_ray_3d(
        config['b'],
        theta_angle=config['theta'],
        phi_angle=config['phi']
    )
    rays_3d.append({
        'x': x, 'y': y, 'z': z, 'r': r,
        'color': config['color'],
        'type': config['type']
    })
    
    # Straight ray
    x_s, y_s, z_s = create_straight_ray_3d(
        config['b'],
        theta_angle=config['theta'],
        phi_angle=config['phi']
    )
    straight_rays_3d.append({
        'x': x_s, 'y': y_s, 'z': z_s,
        'color': config['color']
    })

# ----------------------------
# Create 3D visualization with FUNNEL-SHAPED WARPED GRID
# ----------------------------
print("Creating 3D funnel-shaped spacetime grid...")

fig = plt.figure(figsize=(14, 10), facecolor='white')
ax = fig.add_subplot(111, projection='3d', facecolor='white')

# Create the funnel-shaped warped Cartesian grid
grid_lines = create_warped_cartesian_grid(grid_extent=PLOT_LIMIT, n_lines=28)

# Determine color for each grid line based on distance from center
for x_line, y_line, z_line in grid_lines:
    # Calculate average distance to determine color
    r_avg = np.mean(np.sqrt(x_line**2 + y_line**2))
    
    # Color gradient: red (near) to orange to blue (far)
    if r_avg < 4:
        color = '#DD0000'
        alpha = 0.8
        linewidth = 1.2
    elif r_avg < 7:
        color = '#FF6633'
        alpha = 0.7
        linewidth = 1.0
    elif r_avg < 10:
        color = '#FFAA55'
        alpha = 0.6
        linewidth = 0.9
    else:
        color = '#4488FF'
        alpha = 0.5
        linewidth = 0.8
    
    ax.plot(x_line, y_line, z_line, color=color, alpha=alpha, linewidth=linewidth, zorder=2)

# Add radial grid lines down the funnel
radial_lines = create_radial_grid_lines_funnel(n_radial=20)
for x_line, y_line, z_line in radial_lines:
    ax.plot(x_line, y_line, z_line, color='#DD3333', alpha=0.6, linewidth=0.9, zorder=2)

# Draw event horizon (black sphere)
u_sphere = np.linspace(0, 2 * np.pi, 40)
v_sphere = np.linspace(0, np.pi, 40)
x_sphere = rs * np.outer(np.cos(u_sphere), np.sin(v_sphere))
y_sphere = rs * np.outer(np.sin(u_sphere), np.sin(v_sphere))
z_sphere = rs * np.outer(np.ones(np.size(u_sphere)), np.cos(v_sphere))
ax.plot_surface(x_sphere, y_sphere, z_sphere, color='black', alpha=1.0, zorder=10)

# Initialize light ray lines and markers
ray_lines = []
straight_lines = []
ray_markers = []

for i, ray in enumerate(rays_3d):
    line, = ax.plot([], [], [], color=ray['color'], linewidth=2.5, 
                   alpha=0.9, zorder=5)
    ray_lines.append(line)
    
    straight_line, = ax.plot([], [], [], color=ray['color'], linewidth=1.5, 
                            linestyle='--', alpha=0.3, zorder=3)
    straight_lines.append(straight_line)
    
    marker = ax.scatter([], [], [], color=ray['color'], s=150, 
                       edgecolors='white', linewidths=2, 
                       alpha=1.0, zorder=15)
    ray_markers.append(marker)

# Styling
ax.set_xlim(-PLOT_LIMIT, PLOT_LIMIT)
ax.set_ylim(-PLOT_LIMIT, PLOT_LIMIT)
ax.set_zlim(-PLOT_LIMIT, PLOT_LIMIT)

ax.set_xlabel('X', color='black', fontsize=10)
ax.set_ylabel('Y', color='black', fontsize=10)
ax.set_zlabel('Z (Warped Spacetime)', color='black', fontsize=10)
ax.set_title('Warped Spacetime Funnel: Black Hole Curvature\n' +
            'Grid shows extreme gravitational warping near event horizon', 
            color='black', fontsize=13, weight='bold', pad=20)

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.grid(True, alpha=0.2, color='gray')
ax.tick_params(colors='black', labelsize=8)

initial_azim = 45
initial_elev = 25
initial_zoom = 1.0
ax.view_init(elev=initial_elev, azim=initial_azim)

# ----------------------------
# INTERACTIVE CONTROLS
# ----------------------------
anim_state = {'running': False, 'frame': 0, 'auto_rotate': False}

plt.subplots_adjust(left=0.05, right=0.95, bottom=0.25, top=0.95)

slider_color = 'lightgoldenrodyellow'

ax_azim = plt.axes([0.15, 0.15, 0.65, 0.02], facecolor=slider_color)
slider_azim = Slider(ax_azim, 'Rotate (Azimuth)', 0, 360, valinit=initial_azim, valstep=1)

ax_elev = plt.axes([0.15, 0.11, 0.65, 0.02], facecolor=slider_color)
slider_elev = Slider(ax_elev, 'Tilt (Elevation)', -90, 90, valinit=initial_elev, valstep=1)

ax_zoom = plt.axes([0.15, 0.07, 0.65, 0.02], facecolor=slider_color)
slider_zoom = Slider(ax_zoom, 'Zoom', 0.5, 2.0, valinit=initial_zoom, valstep=0.1)

def update_view(val):
    if not anim_state['auto_rotate']:
        azim = slider_azim.val
        elev = slider_elev.val
        ax.view_init(elev=elev, azim=azim)
        
        zoom = slider_zoom.val
        limit = PLOT_LIMIT / zoom
        ax.set_xlim(-limit, limit)
        ax.set_ylim(-limit, limit)
        ax.set_zlim(-limit, limit)
        
        fig.canvas.draw_idle()

slider_azim.on_changed(update_view)
slider_elev.on_changed(update_view)
slider_zoom.on_changed(update_view)

ax_play = plt.axes([0.15, 0.02, 0.08, 0.03])
btn_play = Button(ax_play, '▶ Play', color='lightgreen', hovercolor='green')

ax_pause = plt.axes([0.24, 0.02, 0.08, 0.03])
btn_pause = Button(ax_pause, '⏸ Pause', color='lightcoral', hovercolor='red')

ax_auto = plt.axes([0.33, 0.02, 0.12, 0.03])
btn_auto = Button(ax_auto, 'Auto-Rotate: OFF', color='lightblue', hovercolor='blue')

def play_animation(event):
    anim_state['running'] = True

def pause_animation(event):
    anim_state['running'] = False

def toggle_auto_rotate(event):
    anim_state['auto_rotate'] = not anim_state['auto_rotate']
    btn_auto.label.set_text('Auto-Rotate: ON' if anim_state['auto_rotate'] else 'Auto-Rotate: OFF')

btn_play.on_clicked(play_animation)
btn_pause.on_clicked(pause_animation)
btn_auto.on_clicked(toggle_auto_rotate)

# ----------------------------
# Animation functions
# ----------------------------
def init():
    for line in ray_lines + straight_lines:
        line.set_data([], [])
        line.set_3d_properties([])
    for marker in ray_markers:
        marker._offsets3d = ([], [], [])
    return ray_lines + straight_lines + ray_markers

def animate(frame):
    if not anim_state['running']:
        return ray_lines + straight_lines + ray_markers
    
    progress = frame / FRAMES
    
    for i, ray in enumerate(rays_3d):
        total_points = len(ray['x'])
        
        if progress < 0.8:
            end_idx = int(progress * total_points / 0.8)
        else:
            end_idx = total_points
        
        if end_idx > 1:
            ray_lines[i].set_data(ray['x'][:end_idx], ray['y'][:end_idx])
            ray_lines[i].set_3d_properties(ray['z'][:end_idx])
            
            marker_idx = min(end_idx - 1, total_points - 1)
            ray_markers[i]._offsets3d = (
                [ray['x'][marker_idx]], 
                [ray['y'][marker_idx]], 
                [ray['z'][marker_idx]]
            )
        
        straight_ray = straight_rays_3d[i]
        straight_lines[i].set_data(straight_ray['x'], straight_ray['y'])
        straight_lines[i].set_3d_properties(straight_ray['z'])
    
    if anim_state['auto_rotate']:
        new_azim = (slider_azim.val + 1) % 360
        slider_azim.set_val(new_azim)
        ax.view_init(elev=slider_elev.val, azim=new_azim)
    
    return ray_lines + straight_lines + ray_markers

# Create animation
print("Generating animation...")
anim = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=FRAMES, interval=INTERVAL_MS, 
                              blit=False, repeat=True)

if SAVE_ANIMATION:
    print("Saving 3D animation as GIF...")
    try:
        from matplotlib.animation import PillowWriter
        writer = PillowWriter(fps=1000//INTERVAL_MS)
        anim.save(ANIMATION_FILENAME, writer=writer, dpi=DPI)
        print(f"✓ Successfully saved: {ANIMATION_FILENAME}")
    except Exception as e:
        print(f"Note: {e}")

print("\n🌌 TRUE 3D Spacetime Grid Visualization Ready!")
print("Use sliders to rotate, tilt, and zoom the 3D view")
print("Click Play to animate photon trajectories\n")
plt.show()
