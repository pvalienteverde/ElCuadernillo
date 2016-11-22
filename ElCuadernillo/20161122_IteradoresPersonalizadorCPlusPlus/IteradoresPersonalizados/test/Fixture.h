/*
 * Fixture.h
 *
 *  Created on: Nov 9, 2016
 *      Author: Pedro Valiente Verde
 */

#ifndef ITERADOR_TESTS_FIXTURE_H_
#define ITERADOR_TESTS_FIXTURE_H_

#include "include/Domicilio.h"
#include <functional>

namespace IteradoresPersonalizados {
namespace tests {
/**
 * Estructura que facilita los datos de los tests
 */
struct Fixture {

	Fixture(size_t numero_de_domicilios = 100, int codigo_postal_test = 29001,
			int codigo_postal_inicial = 29000, int codigo_postal_final = 29003);

	/**
	 * Filtro generico
	 * @param filtro
	 * @param domicilio
	 * @return
	 */
	static bool Filtro(int filtro, const Domicilio &domicilio);

	// Atributos
	std::vector<Domicilio> domicilios;
	std::vector<Domicilio> target_domicilios_filtrados;
	int codigo_postal_test;
	int target_numero_huespedes;
	int target_numero_domicilios;
	std::vector<std::string> target_str_domicilios;
	const std::function<bool(Domicilio)> filtro;

};
}
}

#endif

