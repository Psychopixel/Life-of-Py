# Life-of-Py
Life of Py is artificial creatures simulation world
Detailed Specification (C++ Version)
version 0.0.1

1. World Structure
1.1 Grid Dimensions
Use a square grid with dimensions 1000x1000 cells.
For future flexibility, the grid size may still be set via a config file or .env-like mechanism. But the target build will handle the large 1000x1000 size.
1.2 Cell Occupancy
Only one entity may permanently occupy a cell (plant, prey, predator, or food).
No coexistence of multiple entities in a single cell.
If two creatures try to move into the same cell during an update, the first updater in sequence claims it; the second is blocked or forced to resolve conflict.
1.3 Initial Distribution
The simulation can have thousands of individuals per species (e.g., up to 3,000–5,000 plants/prey/predators each, or even more).
The initial counts for each species are read from a configuration file:
Place plants first (in random free cells).
Then place prey in remaining free cells.
Then place predators in the still-free cells.
Future expansions might allow dynamic spawning during the simulation if needed.
2. Entity Types and Their Mechanics
2.1 Plants
Growth and Reproduction

Each plant matures after a configurable number of ticks.
Upon maturity, it attempts to duplicate into one of the eight adjacent cells if any is free.
If no adjacent cell is free, reproduction is skipped.
Spontaneous Generation

Every N ticks (or continuously each tick with a certain probability), a random empty cell might spawn a new plant.
Death

Plants do not die of old age.
If eaten by prey, the plant disappears, transferring its nutritional energy to the prey.
Energy

A plant’s “energy” is purely for nutritional value; the plant does not consume energy itself.
2.2 Prey
Energy

Each prey has an initial energy, a maximum energy cap, and a tick-based consumption for moves.
If energy hits 0, the prey dies immediately, leaving 1 unit of food.
Movement

In its update turn, a prey can rotate (90° left or right) or move forward 1 cell.
Each action has an energy cost (configurable).
Prey are blocked by cells occupied by other prey (treated like walls), and if they attempt to move onto a predator, they get eaten.
Feeding

Prey only eat plants.
When they enter a cell with a plant, they stop and eat it immediately, gaining energy up to their cap.
Reproduction

After N ticks (configurable) and if energy ≥ reproduction threshold, they duplicate into an adjacent free cell.
Skipped if no adjacent cell is free.
Death

By starvation (energy=0), leaves 1 unit of food.
By being eaten (predator attack), leaves behind food worth a configurable percentage of its remaining energy.
2.3 Predators
Energy

Similar to prey: an initial energy, a maximum cap, energy costs for movement.
If energy = 0, the predator dies, leaving 1 unit of food.
Movement

Same basic actions: rotate or move forward.
They cannot pass through other predators (treated like walls).
If they move onto a cell with a prey, they eat the prey.
Feeding

Predators eat:
Live prey (immediate upon moving into the cell).
Residual food from dead creatures.
If the energy gained exceeds their cap, the excess remains as food in the cell.
Priority: eat prey first, then leftover food (if they still have capacity).
Reproduction

After N ticks + sufficient energy, a predator duplicates into an adjacent free cell.
Skipped if no free cell is available.
Death

Only from hunger in this initial design (energy=0) or future mechanics.
2.4 Food
Origin

Dropped by prey or predators when they die.
Created when a predator overeats (excess energy).
Nutritional Value

1 if a creature starves.
A configurable percentage of energy if a prey/predator was killed by a predator.
Predators can eat this; prey do not.
Deterioration

Food decays over time; after X ticks, its value diminishes to 0 and it disappears.
Multiple food items in the same cell are combined into a single entity (sum of values).
Cell Occupancy

A cell with food is considered “occupied” for new spawns (no new plant, etc.), but creatures can move through it and eat.
3. Turn Management and Update Order
3.1 Random Entity List
Each tick, gather all entities into a list.
Shuffle or randomize periodically (e.g., every frame, every few frames, or every N ticks) to avoid bias.
3.2 Sequential Update
Process each entity in the list:
If it’s active, let it act (grow, move, eat, etc.).
If it dies during its update, immediately replace/remove it from the list.
If it’s already inactive, ignore it.
3.3 Cleanup
End of each tick:
Remove all flagged “dead” entities definitively.
Update food deterioration; remove food entities that hit 0 value.
4. Energy, Movement, and FPS Considerations
4.1 Parameters
Initial energy, max energy cap, cost to move forward, cost to rotate, limit of energy spent on moves per tick, etc.
The parameter file / config is critical for fine-tuning behavior.
4.2 Movement Limit
Each entity can only spend up to X energy points on movement each tick. If it tries to exceed this, the action is disallowed or truncated.
4.3 60 FPS Real-Time Update
Target a 60 frames per second rendering rate.
Potential approaches:
Lockstep: run the entire simulation tick, then render. If the simulation is too large to finish a tick in <16ms, it may drop frames or run slower than real time.
Variable Time Step: separate the simulation loop from the rendering loop. The simulation might run asynchronously or in discrete steps, but we aim to keep the display responsive.
Because the grid is 1000x1000 and can contain thousands of entities, performance optimizations will be needed.
5. Neural Network and AI Behavior
5.1 Base Architecture (Initial)
Input (example: 8 values — can expand in future):
Normalized energy (0–1).
Time to reproduction (0–1).
Left view – type (0=empty, 1=plant, 2=prey, 3=predator, 4=food).
Left view – distance (0–1).
Front view – type (0–4).
Front view – distance (0–1).
Right view – type (0–4).
Right view – distance (0–1).
Hidden Layer: ~10 neurons, ReLU activation (configurable).
Output (4 neurons):
Stay still
Turn left 90°
Turn right 90°
Move forward 1 cell
5.2 Action Selection
Perform a forward pass, obtain 4 values, pick the highest (argmax).
If insufficient energy or it would exceed the per-turn move cost, fallback to another valid action or “stay still.”
5.3 Evolution and Mutation
Fixed network topology for each species.
Mutation on weight values: random noise added upon reproduction (controlled by mutation probability and standard deviation).
In the future, we may consider multi-layer networks or advanced architectures (e.g. CNNs, NEAT-like dynamic topology).
6. Interface and Visualization
6.1 2D Display
A 2D grid representation showing:
Plants, Prey, Predators, Food.
Possibly color-coded tiles or sprite-based icons.
Libraries to consider: SDL2, SFML, or a custom OpenGL approach.
The update frequency of the visual layer should aim for 60 FPS if possible.
6.2 Pause and Inspection
A Pause feature: halt the simulation updates while still rendering the static scene.
Click on an Entity:
Highlight the cell/creature.
Option to save/copy or inspect the creature’s neural network (weights, biases, current energy, etc.).
This might open a small info window or console output.
6.3 Population Graphs
Real-time or near real-time charts (line graphs or bar graphs) showing:
Current count of Plants, Prey, and Predators over time.
Could be integrated in a side panel or a separate debug overlay.
Update every few ticks or once per second to reduce overhead.
6.4 Ticks and Time
Display tick count and simulated time.
Possibly display real-world time since simulation start.
7. Code Architecture and Implementation Details
7.1 Class Organization
World

Holds:
Grid data structure (1000x1000).
List of all entities (plants, prey, predators, food).
Manages:
Initialization (random placement).
Each simulation tick (building the entity list, shuffling, calling updates, cleanup).
Communication with the rendering system (optional or via a separate Renderer class).
Entity (abstract/base)

Common attributes: position, entity type, pointer to the World, etc.
Virtual methods: update(), die(), etc.
Plant, Prey, Predator, Food (derived from Entity)

Each overrides update() with specific behaviors.
Prey and Predator might store a pointer or an instance of NeuralNetwork (for AI-driven movement decisions).
NeuralNetwork

Stores weights, biases for the MLP.
Methods for forward() (pass input → output) and mutate() (adjust weights).
Possibly templated or can use standard containers (e.g., std::vector<float>).
If future GPU acceleration is desired:
Provide a CPU-based path first.
Potentially add CUDA kernels for forward pass if we scale up to handle many creatures in parallel.
Renderer (optional separate component)

Responsible for drawing the grid.
Could manage a texture atlas or sprites for different entity types.
Config / Parameters

A structure or singleton that loads from a .env or .ini file:
Grid size, initial populations, energy costs, mutation rates, reproduction thresholds, etc.
7.2 Main Loop Outline
cpp
Copia codice
int main() {
    // 1. Load configuration (grid size, etc.)
    Config config = Config::LoadFromFile("simulation_config.ini");

    // 2. Initialize the World
    World world(config);
    world.initialize();

    // 3. Initialize Renderer
    Renderer renderer(config, world);

    // 4. Main loop
    bool running = true;
    bool paused = false;
    while(running) {
        // Handle input (pause, close, click on entity, etc.)
        handleEvents(paused, running, world, renderer);

        if (!paused) {
            // Update the world
            world.update();
        }

        // Render the scene
        renderer.draw();

        // Limit to ~60 FPS
        limitFramerate(60);
    }

    return 0;
}
7.3 Single-Threading with CPU-Based Simulation
Single-threaded design for clarity in the initial version.
Later expansions might implement multi-threading or GPU acceleration if performance is insufficient.
7.4 GPU Acceleration (Future)
The design will keep in mind that:
NeuralNetwork could have a GPU-based forward pass.
We might move collision checks or entity updates to GPU if they become bottlenecks.
This will require additional CMake configurations and CUDA toolchain integration.
8. Performance Targets and Optimizations
Thousands of Creatures

We may have well over 10,000 total entities in the grid (e.g., 3000 prey, 3000 predators, 4000 plants, etc.).
The update loop must handle each entity’s logic quickly.
60 FPS

For real-time rendering, the total update + render time per frame should ideally be < 16ms.
Large-scale collisions, pathfinding, and neural net evaluation could be optimized using data-oriented designs (e.g., storing entity info in contiguous arrays, efficient memory usage, etc.).
Spatial Partitioning (Optional)

Could use quad-trees, grids, or other structures to quickly find neighbors or detect collisions.
The 1000x1000 grid might naturally be used as a large 2D array, which can be efficient if carefully implemented.
Deferred Rendering

Only redraw cells that changed.
Or keep it simple and redraw everything each frame but using efficient techniques (hardware acceleration, sprite batches, etc.).
9. Pause, Inspection, and Neural Network Editing
A pause button (e.g., press Space or P).
When paused, the user can click on a cell (using the mouse in the 2D view) to:
Identify if an entity is present.
Open an overlay or panel showing:
Entity type (Prey, Predator, etc.).
Current energy, age, next reproduction tick, etc.
A dump of the neural network weights/biases (which can be saved to a file or clipboard).
Potentially allow for manually editing weights or forcibly mutating them for experimentation.
10. Conclusion
This final specification integrates the large grid (1000x1000), thousands of entities per species, a 2D display at 60 FPS, pause/inspection features, and a CPU-based approach with the option for future GPU acceleration. The single-threaded design ensures simpler initial implementation, while the code architecture is flexible enough to add multi-threading, more complex neural networks, or CUDA support later.

Key next steps:

Prototype the data structures (grid, entity list, neural nets).
Implement the main simulation loop (update + render).
Optimize for performance to reach near real-time frame rates.
Add interactive capabilities (pause, click, inspect).
Expand the neural network or GPU usage if performance or complexity demands it.
