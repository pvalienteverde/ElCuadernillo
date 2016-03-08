
#Optimización Del Gradiente Descendente aplicando el Momento por medio de TensorFlow

** El algoritmo se implenta a partir del calculo de gradientes que nos sumistra TensorFlow, de esta manera se da un ejemplo de como implementar cualquier algoritmo que tenga como base el gradiente descendente**

Material correspondiente a la entrada del [post](http://www.p.valienteverde.com/tensorflow-mini-batch-gradiente-descendente-momento) 

* **gradient_descent_with_momentum.py** : Modulo donde se encuentra todas las funciones que se utilizan en los ipython

* **GradientDescentWithMoment.ipynb** : Ipython con la demostración

* **GradientDescentWithMomentPlots.ipynb** : Ipython configurado para generar informes por medio de TensorBoard. Por defecto se genera en la ruta definida por el parametro <code>ruta_sumario</code> : 
	- <code>ruta_sumario='/tmp/logs_tensor_flow/sgd_momentum'</code> 
Para ejecutar el resumen unicamente abre una terminal y pega (Solamente funciona con chrome):
<code>tensorboard --logdir /tmp/logs_tensor_flow/sgd_momentum/</code>

