import numpy as np
import tensorflow as tf
import time

def generar_muestra(grado:int, tamano:int=100000, intervalo_x:list=[-2, 2]):
    '''
    Generar de muestras
    
    :param grado:
    :param tamano:
    :param intervalo_x:
    '''

    coeficentes = (-10)*np.random.ranf(grado)+5
    x = np.linspace(intervalo_x[0],intervalo_x[1],tamano)
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

def regression_gradient_descent(train_x,train_y,iteraciones_maximas=10000,diff_error_parada=1e-3,learning_rate_inicial=1e-2):    
    '''
    Regresion Multiple utilizando gradiente descendente, optimiza error cuadratico medio (ECM)
    
    :param train_x:
    :param train_y:
    :param iteraciones_maximas:
    :param diff_error_parada:
    :param learning_rate_inicial:
    '''
    
    
    error_por_iteracion_gd=[np.nan]
    grafo_regresion_multiple = tf.Graph()
    with grafo_regresion_multiple.as_default():
        
        # Entrada de los datos
        datos_entrada = tf.placeholder(dtype=tf.float32,shape=train_x.shape)
        datos_salida = tf.placeholder(dtype=tf.float32,shape=train_y.shape)           
                
        # Inicilizacion de la variable
        pesos = tf.Variable(tf.zeros([datos_entrada.get_shape()[1], 1]))
        
        # Definimos funcion coste
        output = tf.matmul(datos_entrada,pesos)        
        residuos = output - datos_salida
        ecm = tf.reduce_mean(tf.square(residuos),name='ecm')
        
        optimizador = tf.train.GradientDescentOptimizer(learning_rate_inicial,name="Optimizador").minimize(ecm)
    
    ti_gd = time.time()    
    with tf.Session(graph=grafo_regresion_multiple) as sesion_SG:
        tf.initialize_all_variables().run()
        condicion_parada=0
        for iteracion in range(iteraciones_maximas):    
            _,p,e_ite= sesion_SG.run([optimizador,pesos,ecm],feed_dict={datos_entrada:train_x,datos_salida:train_y})        
            condicion_parada=np.abs(error_por_iteracion_gd[-1]-e_ite)<diff_error_parada
            error_por_iteracion_gd.append(e_ite)
            if iteracion % 200 == 0 or condicion_parada:
                print("Iteracion {}:\n\tPesos: {}\n\tecm: {}".format(iteracion,p.ravel(),e_ite))
    
                if condicion_parada:
                    print("-------------------------------------------------------------------------")
                    print("Iteracion {}:\n\tPesos: {}\n\tecm: {}".format(iteracion,p.ravel(),e_ite))
                    print("-------------------------------------------------------------------------")
                    break
            if condicion_parada:
                break
            
    tf_gd = time.time()
    print ("Tiempo de calculo: {}".format(tf_gd-ti_gd))
    return p,e_ite,error_por_iteracion_gd

def get_minibatches(x_train,y_train,indices):
    '''
    Generador de mini_batch dado un indice
    :param x_train:
    :param y_train:
    :param indices:
    '''       
    for idx in indices:        
        yield x_train[idx],y_train[idx]
        

def regression_stochastic_gradient_descent (train_x,train_y,num_mini_batch,iteraciones_maximas=10000,diff_error_parada=1e-3,learning_rate_inicial=1e-2):
    '''
    Regresion multiple utilizando gradiente descendente por medio de mini batches
    
    :param train_x:
    :param train_y:
    :param num_mini_batch:
    :param iteraciones_maximas:
    :param diff_error_parada:
    :param learning_rate_inicial:
    '''    
    
    tamano_train_x=train_x.shape
    elementos_por_grupo=tamano_train_x[0]/num_mini_batch
    iteraciones_maximas_mini=int(iteraciones_maximas/num_mini_batch)
    error_por_iteracion_sgd=[np.nan]
    ite_reales=0
    
    grafo_regresion_multiple_mini = tf.Graph()
    with grafo_regresion_multiple_mini.as_default():
        
        # Entrada de los datos
        datos_entrada = tf.placeholder(dtype=tf.float32,shape=[elementos_por_grupo,tamano_train_x[1]])
        datos_salida = tf.placeholder(dtype=tf.float32,shape=[elementos_por_grupo,1])           
                
        # Inicilizacion de la variable
        pesos = tf.Variable(tf.zeros([datos_entrada.get_shape()[1], 1]))
        
        # Definimos funcion coste
        output = tf.matmul(datos_entrada,pesos)        
        residuos = output - datos_salida
        ecm = tf.reduce_mean(tf.square(residuos),name='ecm')
        
        optimizador = tf.train.GradientDescentOptimizer(learning_rate_inicial,name="Optimizador").minimize(ecm)
    
    ti_gd = time.time()    
    with tf.Session(graph=grafo_regresion_multiple_mini) as sesion_SGD:
        tf.initialize_all_variables().run()
        condicion_parada=0
        for _ in range(iteraciones_maximas_mini):
            
            indices=np.arange(tamano_train_x[0])
            np.random.shuffle(indices)
            generados_minibatches=get_minibatches(train_x,train_y,indices.reshape((num_mini_batch,-1)))
            
            for x_mini,y_mini  in generados_minibatches:
                _,p,e_ite= sesion_SGD.run([optimizador,pesos,ecm],feed_dict={datos_entrada:x_mini,datos_salida:y_mini})        
                condicion_parada=np.abs(error_por_iteracion_sgd[-1]-e_ite)<diff_error_parada
                error_por_iteracion_sgd.append(e_ite)
                ite_reales+=1
                
                if ite_reales % 200 == 0:
                    print("Iteracion {}:\n\tPesos: {}\n\tecm: {}".format(ite_reales,p.ravel(),e_ite))
    
                if condicion_parada:
                    print("-------------------------------------------------------------------------")
                    print("Iteracion {}:\n\tPesos: {}\n\tecm: {}".format(ite_reales,p.ravel(),e_ite))
                    print("-------------------------------------------------------------------------")
                    break
            if condicion_parada:
                break        

    tf_gd = time.time()
    print ("Tiempo de calculo: {}".format(tf_gd-ti_gd))        
    return p,e_ite,error_por_iteracion_sgd

