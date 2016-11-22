/*
 * Domicilio.h
 *
 *  Created on: Nov 20, 2016
 *      Author: pedro
 */

#ifndef DOMICILIO_H_
#define DOMICILIO_H_

#include <string>
#include <vector>
#include <random>
#include <algorithm>
#include <iostream>

namespace IteradoresPersonalizados {

/**
 * Clase de apoyo a los ejemplos
 */
class Domicilio {
public:
	Domicilio(int codigo_postal, int huespedes, std::string informacion = "");
	~Domicilio() = default;

	/**
	 * Getters de atributos
	 * @return
	 */
	int CodigoPostal() const;
	int Huespedes() const;

	/**
	 * Setter y getter de Informacion
	 * @param informacion
	 */
	void Informacion(const std::string &informacion);
	std::string Informacion() const;
	std::string ToString() const;

	/**
	 * Se genera una lista de domicilios entre los codigos postales especificados
	 * @param numero_de_domicilios
	 * @param codigo_postal_inicial
	 * @param codigo_postal_final
	 * @return
	 */
	static std::vector<Domicilio> DomiciliosRandom(size_t numero_de_domicilios,
			int codigo_postal_inicial, int codigo_postal_final);

	/**
	 * Operador de desigualdad, imprecindible para comparar
	 * @param rhs
	 * @return
	 */
	bool operator!=(const Domicilio& rhs);


private:
	int codigo_postal;
	int huespedes;
	std::string informacion;
	int id;
	static int numero_domicilios_totales; // Contador de los objetos generados de Domicilio

};

std::ostream& operator<<(std::ostream& out, const Domicilio& f);

}
#endif /* DOMICILIO_H_ */
