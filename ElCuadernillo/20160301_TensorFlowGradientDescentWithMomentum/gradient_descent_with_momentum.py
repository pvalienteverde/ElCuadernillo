'''
Created on Mar 1, 2016

@author: pedro valiente verde
'''
import numpy as np
import tensorflow as tf
import time
"""
Ejemplo practico para modificicar los gradientes descendentes que nos 
suministra tensorflow antes de aplicarlos

p.valienteverde.com

"""

def get_minibatches(x_train, y_train, indices):
    
    '''
    Generador de mini_batch dado un indice
    :param x_train:
    :param y_train:
    :param indices:
    '''
           
    for idx in indices:        
        yield x_train[idx], y_train[idx]
        
def generar_muestra(grado:int, tamano:int=100000, intervalo_x:list=[-2, 2]):
    '''
    Generar de muestras
    
    :param grado:
    :param tamano:
    :param intervalo_x:
    '''

    coeficentes = (-10) * np.random.ranf(grado) + 5
    x = np.linspace(intervalo_x[0], intervalo_x[1], tamano)
    y = np.polynomial.polynomial.polyval(x, coeficentes)
    return x, y, coeficentes

def generar_matriz_coeficientes(datos:np.array, grado:int=1):
    '''
    Genera la matriz A (Ax=B)
    
    :param datos:
    :param grado:
    '''
   
    matriz_coeficientes = np.ones((len(datos), grado), dtype=np.float32)
    for elevado in range(1, grado):
        matriz_coeficientes[:, elevado] = np.power(datos, elevado)
    
    return matriz_coeficientes   



        

def gradient_descent_with_momentum (train_x,
                                    train_y,
                                    num_mini_batch=1,
                                    iteraciones_maximas=10000,
                                    diff_error_parada=1e-3,
                                    learning_rate_inicial=1e-2,
                                    momentum=0.95,
                                    activar_sumario=False,
                                    ruta_sumario='/tmp/logs_tensor_flow/sgd_momentum',
                                    prefijo=''):
    '''
    Gradiente Descendente Estocastico/Mini-batch con la extensión del Momento. 
    :param train_x: Observaciones
    :param train_y: Output
    :param num_mini_batch: Hiperparametro, Numero de cada mini_batch, si no especifica nada, será el lote completo(GradientDescent)
    :param iteraciones_maximas: Condicion de parada, numero maximo de iteraciones
    :param diff_error_parada: Condicion de parada, diferencia minima entre iteraciones que se puede alcanzar
    :param learning_rate_inicial: Hiperparametro, tasa de entrenamiento
    :param momentum: Hiperparametro, coeficiente del factor del momento: 
                     [0,1] --> 0: No se aplica la extension del momento
    :param activar_sumario: Activa el resumen del algorimo guardandolo donde indique el argumento ruta_sumario
    :param ruta_sumario: ruta donde se guarda el resumen del algorimo
    :param prefijo: Prefijo de las variables dentro del resumen, de esta manera se puede comparar dentro de un mismo resumen, distintas configuraciones
    '''
    np.set_printoptions(precision=2)
    def minimizar(optimizador, funcion_coste, acumulador, learning_rate_iniciaL_tf, rate_momemtum_tf):
        '''
        
        :param optimizador: clase que suministra los gradientes
        :param funcion_coste: funcion a minimizar
        :param acumulador: acumulador del momento, inercia acumulada
        :param learning_rate_iniciaL_tf: tasa de aprendizaje
        :param rate_momemtum_tf: tasa del momento
        '''
        
        grads_and_vars = optimizador.compute_gradients(funcion_coste)
        grads = []
        vars = []
        for grad, var in grads_and_vars:
            if grad is None:
                grads.append(grad)
                vars.append(var)
                continue
            
            # accum = accum * momentum + grad
            accum_aux = tf.add(tf.mul(rate_momemtum_tf, acumulador), grad)
            accum_op = tf.assign(acumulador, accum_aux)
                               
            grads.append(accum_aux)
            vars.append(var)

       
        with tf.control_dependencies([accum_op]):  
            # var = var - lr * accum 
            optimizar = optimizador.apply_gradients(zip(grads, vars))
            
        return optimizar    
    
    tamano_train_x = train_x.shape
    elementos_por_grupo = tamano_train_x[0] / num_mini_batch
    
    grafo_regresion_multiple_mini = tf.Graph()
    with grafo_regresion_multiple_mini.as_default():
        
        # Entrada de los datos
        datos_entrada = tf.placeholder(dtype=tf.float32, shape=[elementos_por_grupo, tamano_train_x[1]])
        datos_salida = tf.placeholder(dtype=tf.float32, shape=[elementos_por_grupo, 1])           
        learning_rate_iniciaL_tf = tf.constant(learning_rate_inicial, dtype=tf.float32)
        rate_momemtum_tf = tf.constant(momentum, dtype=tf.float32)
                
        # Inicilizacion de la variable
        pesos = tf.Variable(tf.zeros([datos_entrada.get_shape()[1], 1]))        
        acumulador = tf.Variable(tf.zeros([datos_entrada.get_shape()[1], 1]))
        
          
        # Definimos funcion coste
        output = tf.matmul(datos_entrada, pesos)        
        residuos = output - datos_salida
        ecm = tf.reduce_mean(tf.square(residuos), name=prefijo + 'ecm')        
        
        
        optimizador = tf.train.GradientDescentOptimizer(learning_rate_inicial, name=prefijo + "Optimizador")        
        optimizar = minimizar(optimizador, ecm, acumulador, learning_rate_iniciaL_tf, rate_momemtum_tf)
    
        if activar_sumario:
            tf.histogram_summary(prefijo + 'pesos', pesos)
            tf.histogram_summary(prefijo + 'acumulador', acumulador)
            tf.scalar_summary(ecm.op.name, ecm)
            sumario_op = tf.merge_all_summaries()
    
    iteraciones=0
    diff_error=np.NaN
    ti_gd = time.time()
    np.set_printoptions(precision=2)
    error_entrenamiento=np.NaN
    with tf.Session(graph=grafo_regresion_multiple_mini) as sesion_SGD:
        tf.initialize_all_variables().run()
        condicion_parada = 0
        if activar_sumario:
            sumario = tf.train.SummaryWriter(ruta_sumario, sesion_SGD.graph_def)
        while(1):
    
            generados_minibatches=[(train_x,train_y)]
            if not num_mini_batch==1:
                indices = np.arange(train_x.shape[0])
                np.random.shuffle(indices)
                generados_minibatches = get_minibatches(train_x, train_y, indices.reshape((num_mini_batch, -1)))
                
            for x_mini, y_mini  in generados_minibatches:
                if activar_sumario:
                    _, pesos_np, error_entrenamiento, sumario_iteracion = sesion_SGD.run([optimizar, pesos, ecm, sumario_op], feed_dict={datos_entrada:x_mini, datos_salida:y_mini})        
                    sumario.add_summary(sumario_iteracion, iteraciones)
                else: 
                    _, pesos_np, error_entrenamiento = sesion_SGD.run([optimizar, pesos, ecm], feed_dict={datos_entrada:x_mini, datos_salida:y_mini})        
                condicion_parada = np.abs(diff_error - error_entrenamiento) < diff_error_parada
                diff_error=error_entrenamiento
                iteraciones += 1
                    
                if iteraciones % 500 == 0:
                    print("Iteracion {}:\n\tPesos: {}\n\tecm: {}".format(iteraciones, pesos_np.ravel(), error_entrenamiento))
        
                if condicion_parada or iteraciones>iteraciones_maximas or error_entrenamiento==np.inf:                        
                    break
                                        
                    
            if condicion_parada or iteraciones>iteraciones_maximas or error_entrenamiento==np.inf:
                break
                
    
    tf_gd = time.time()
    tiempo_calculo = tf_gd - ti_gd
        
    print("Iteracion {}:\n\tPesos: {}\n\tecm: {}".format(iteraciones, pesos_np.ravel(), error_entrenamiento))
    print ("Tiempo de calculo: {}".format(tiempo_calculo))
    print("----------------------")    
    return pesos_np, error_entrenamiento, tiempo_calculo
