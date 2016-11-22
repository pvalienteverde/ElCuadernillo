/*
 * Fixture.cpp
 *
 *  Created on: Nov 22, 2016
 *      Author: pedro
 */

#include "Fixture.h"
using namespace IteradoresPersonalizados::tests;

Fixture::Fixture(size_t numero_de_domicilios, int codigo_postal_test,
		int codigo_postal_inicial, int codigo_postal_final) :
		domicilios(
				Domicilio::DomiciliosRandom(numero_de_domicilios,
						codigo_postal_inicial, codigo_postal_final)), codigo_postal_test(
				codigo_postal_test), target_numero_huespedes(0), target_numero_domicilios(
				0), filtro(
				std::bind(Filtro, codigo_postal_test, std::placeholders::_1)) // != [&](Domicilio domicilio) {return domicilio.CodigoPostal()==codigo_postal_test;}
{

	/**
	 * Generamos el resultado que esperamos de los tests
	 * de forma tradicional
	 */
	for (auto &domicilio : domicilios) {
		if (filtro(domicilio)) {
			domicilio.Informacion("Domicilio chequeado");
			target_domicilios_filtrados.push_back(domicilio);
			target_numero_huespedes += domicilio.Huespedes();
			target_numero_domicilios++;
		}
		target_str_domicilios.push_back(domicilio.ToString());
	}

}

/**
 * Filtro generico
 * @param filtro
 * @param domicilio
 * @return
 */
bool Fixture::Filtro(int filtro, const Domicilio &domicilio) {
	return domicilio.CodigoPostal() == filtro;
}
