# Value Prediction for Input Data Commonality
Contemporary applications operate on real-world inputs where spatially correlated data points bear strong resemblance. However, these data reside in memory as independent blocks, and loading from any new data point incurs long memory latency. To hide the latency with data commonalities, we propose that a load instruction speculate the value loaded upon cache miss based on its previously seen values which are highly likely similar.

## Data Commonality
Many data-driven applications consume data collected from the real world that have the following properties:
- Massive input data
- Continuous, predictable pattern
- Highly similar at spatially correlated locations 
- Time-sensitive, only used once during a small time window

These properties are not ideal to the current control-flow driven hardware architecture, which assumes uncorrelated data points and rely on cache to predict future data usage. 

This study adapts **Value Prediction** to accelerate these applications. Value prediction predicts the loaded value from the memory before the load completes to hide the load latency. The following instructions that depend on the data block can use the speculated value for calculation, and a squash happens when the prediction is wrong, like for a branch misprediction. 

Value prediction works best for data blocks that are first seen but have same values as data blocks previously seen. We expect value prediction to bring performance benefits for applications described above because they have rare data reuse but high data commonalities. 

Specifically, there are two types of data commonalities that the study tries to address:
1. Adjacent data similarities, because the data points are contiguous and neighboring data are most likely similar. 
2. Spatially correlated data similarities. Data may come in batches and similar data patterns will occur after fixed strides. 

Below graph shows two adjacent image frames in a dash camera video streaming, taken from the Tulane self-driving dataset.

![](https://user-images.githubusercontent.com/49755429/211525458-d24c3be6-963c-40f6-90af-25ab09303e31.PNG)

These properties hold for other contiguous data, such as sensors, monitors and camera frames. 

## Micro-arch Exploitation

Value prediction is done on the microarchitecture level: each load instruction speculate the value based on its load history. We observed that correlated data points are likely loaded by the same load instruction, both for adjacent data (intuitive, inner loops going through a series of input data) and for repetitive patterns (illustrated below). 

![enter image description here](https://user-images.githubusercontent.com/49755429/211525440-06a43794-dd6b-4ecc-8401-97031b27e2b9.PNG)

Design: 
- Predict memory read instructions
- Prediction is triggered at cache miss. The predictor target at the first occurrence of a data block that leads to a miss. 
- Prediction is based on the instruction addresses of load instructions. We use a load instruction's history (previous loaded values with the same instruction PC) to predict upcoming loads, similar to how a branch history table works.

The diagram below shows the location of the predictor (load history cache) in a 5-stage pipeline.

![enter image description here](https://user-images.githubusercontent.com/49755429/211525456-5870b08e-e775-4e54-8093-1255d73a43b0.PNG)

## Analytical Model

Here we estimate how much benefit can be gauged from value prediction by quantifying the data commonalities within input data. Specifically, we used the lane detection workload as an example. We took two adjacent frames and counted the number of pixels that are the same between two frames (R/G/B channels are counted independently). The images and the script used are in [images](./images) folder. This only accounts for spatially correlated data commonality (inter-frame) because it is hard to predict which data the load instruction will access with adjacent data commonality (intra-frame).

Counts with various difference thresholds are shown in the table below. Counts for similar (but not exactly the same) data points are also included because sometimes approximate prediction might also be useful. This study only focuses on exact prediction but there could be future work in the direction of approximation. 

|Data difference|Percentage|
|----------------|-------------------------------|
|Data points with no difference|9%|
|Data points with difference < 5|46%|
|Data points with difference < 10|62%|

## Simulation

### Simulator

We used the CVP software simulator taken from the [competition on Value Prediction](https://www.microarch.org/cvp1/index.html). The simulator takes an instruction-level trace and runs cycle-accurate simulation. It models a general processor that has 5-stage pipeline, 3-level cache hierarchy, a store buffer, a resource scheduler, and a branch predictor. We modified the simulator to accommodate more general ISAs and simulated our streaming applications. Documentation and modified code can be found in the [CVP](./CVP) folder.

### Workloads 

We ran experiments with three different workloads:

- [Sketch](./sketch): Very simple, self-written code that naively goes through a giant array and increment each element. Ideal workload for value prediction. 
	- Evaluated 10x200 array with all elements of the same value
- [MJPEG](./mjpegtools) (Motion-JPEG): Widely-used image processing workloads that does pixel-level compression and transformation. Contiguously accesses fresh new data without doing much work on each. 
	- Evaluated mpeg2enc's core code with only 1 frame of size 1024x368 from lane-detection (because frames are large and inter-frame data similarities cannot be picked up by the predictor)
- [Lane detection](./lane_detection): Algorithm from an autonomous vehicle application set. Input is a collection of images from a streaming dash camera. Theoretically good candidate but has a lot of data reuse and complex access patterns that are not VP-friendly.
	- Evaluated the ATLAS kernel code of 1 frame 

Current experiments focuses on adjacent data similarities because spatially correlated data points are too further away to be spotted by the predictor for large image inputs, but it could be exploited by other workloads with more impact input patterns.

### Results 

Prediction uses the Value Prediction Competition's award-winning predictor that is implemented in software.

|Workload|Perfect Speedup|Prediction Speedup|
|----------------|------------------------|------------------------|
|Sketch|47%|24%|
|MJPEG|39%|8%|
|Lane detection|6%|No speedup|

## Takeaways 

We observe that a simple program and a perfect prediction both work well but are both unrealistic. Real-word applications are complicated and much work remain to improve the predictor for accurate speculations.

We face the following challenges:
- Data points are similar but not exactly the same: a one bit difference in a 32-bit value will trigger a squash, and this is common especially in image frames. This paves the way for future studies on using approximate predictions.
- Data points that are correlated are sometimes further away. If there are nested loops, the load instruction might already be executed several times before it hits the correlated data point, and the load history cache cannot remember too many things, or it is hard to pick from a long history.
- Data reuse is very common. Reuse is favored in today's architecture (temporal cache locality) and today's popular applications (e.g. convolutions in ML). If everything is already cached, value prediction does not help much.
- Sadly most of the high-performance applications are highly optimized towards the current architecture and the data access patterns are largely twisted. Value prediction doesn't work well for these cases so it's hard to evaluate with existing popular applications. 

## Future Work

- Approximation: we can accept values that are almost the same as predicted (this happens pretty often in experiments) if the exact values do not matter that much, for example inputs to some neutral networks
- This is more of a future vision but I think value prediction can make programming more intuitive. Instead of intentionally partitioning or swizzling the data, or using nested loops to exploit cache locality, programmers can write code with simpler memory footprints that enjoy similar performance benefits from speculation.

> Written with [StackEdit](https://stackedit.io/).
