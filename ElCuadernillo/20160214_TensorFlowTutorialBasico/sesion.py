import tensorflow as tf

grafo1 = tf.Graph()
with grafo1.as_default():
    matrix1 = tf.constant([[3., 3.], [3., 3.]], name='Matriz1')
    matrix2 = tf.constant([[2., 2.], [2., 2.]], name='Matriz2')
        
    producto_grafo1 = tf.matmul(matrix1, matrix2, name='Producto')
    
with tf.Session(graph=grafo1) as sess:
    result = sess.run([producto_grafo1])
    print (result)
    
    

