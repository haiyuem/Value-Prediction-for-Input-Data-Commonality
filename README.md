# Value-Prediction-for-Input-Data-Commonality
Contemporary applications operate on real-world inputs where spatially correlated data points bear strong resemblance. However, these data reside in memory as independent blocks, and loading from any new data point incurs long memory latency. To hide the latency with data resemblance, we propose that a load instruction speculate the value loaded upon cache miss based on its previously seen values which are highly likely similar.

## Data Commonality
- massive input data from env
- continuous
- highly similar 

Two types of data commonality: 
**inter** and **intra**
![Two adjacent image frames in a dash camera video streaming, taken from the Tulane self-driving dataset. Abundant data resemblance show up both intra-frame (1) and inter-frame (2).](https://user-images.githubusercontent.com/49755429/211525458-d24c3be6-963c-40f6-90af-25ab09303e31.PNG)
+sensor example: inter and intra

## Micro-arch Exploitation
- use load instructions to speculate values
- works for both inter and intra


## Analytical Model
quantify %similarities in lane detection images TODO

## Simulation

### Simulator
We use CVP, a VP for competition 
CVP website 
CVP code 

### Workloads 
sketch vs. （sketch w/ mjpeg?）mjpeg vs. lane detection

### Results 
table here 


## Takeaways 




> Written with [StackEdit](https://stackedit.io/).
