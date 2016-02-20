import tensorflow as tf

# Se genera un grafo por defecto
const1 = tf.constant(4.0,name='const1')
grafo_por_defecto=tf.get_default_graph()
assert const1.graph is grafo_por_defecto

# En este caso ya no se genera el grafo, unicamente se añade la operación
const2 = tf.constant(30.0,name='const2')
assert const2.graph is grafo_por_defecto

# Explicitamente creamos un nuevo grafo
grafo1 = tf.Graph()
with grafo1.as_default():
    conts3 = tf.constant(30.0)
    assert conts3.graph is grafo1
    
const3 = tf.constant(20)
assert const3.graph is grafo_por_defecto  
