/*
 * TestBasico.cpp
 *
 *  Created on: Nov 9, 2016
 *      Author: Pedro Valiente Verde
 */

/**
 * http://www.boost.org/doc/libs/1_42_0/libs/test/doc/html/utf.html
 *
 * undefined reference to `main' --> #define BOOST_TEST_DYN_LINK
 *
 * En el linker nos pone: undefined reference to `boost::unit_test::framework::master_test_suite()' y mas --> nos falta cargas la libreria boost-test
 * Donde y como se llaman los paquetes:_ sudo dnf repoquery --list boost-test
 *
 */
#include "Fixture.h"
#include <iostream>
#include <algorithm>
#include <numeric>
#include <boost/algorithm/string/join.hpp>
#include <boost/range/adaptor/transformed.hpp>
#include <boost/range/algorithm/copy.hpp>
#include <string>
#include <boost/lexical_cast.hpp>
#include <boost/range/adaptor/filtered.hpp>
#include <boost/range/algorithm/for_each.hpp>
#include "include/WrapperVector.h"

#include <numeric>

#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE TestWrapperUtiles

#include <boost/test/unit_test.hpp>

using namespace IteradoresPersonalizados;

/**
 * En cada uno de los 3 tests se va a comprobar:
 * - Numero de huespedes: Suma de los huespedes del codigo postal elegido
 * - Numero de domicilios: Numero de los domicilios del codigo postal elegido
 * - Modificaremos el atributo info solamente para los del codigo postal elegido
 *   y comprobamos que se ha serializado correctamente con los cambios anteriores
 *
 * En el ultimo tests, mostraremos por pantalla los resultados esperados
 */
BOOST_FIXTURE_TEST_SUITE(iteradores_personalizados,tests::Fixture)

BOOST_AUTO_TEST_CASE( filtro_por_wrappervector ) {

	WrapperVector<Domicilio> wrapper(domicilios, filtro);
	BOOST_CHECK_EQUAL_COLLECTIONS(target_domicilios_filtrados.begin(),
			target_domicilios_filtrados.end(), wrapper.filtro_begin(),
			wrapper.filtro_end());

	int numero_huespedes =
			std::accumulate(wrapper.filtro_begin(), wrapper.filtro_end(), 0,
					[](int acumulador,const Domicilio&domicilio) {return acumulador+domicilio.Huespedes();});
	BOOST_CHECK(numero_huespedes == target_numero_huespedes);

	int numero_domicilios = std::distance(wrapper.filtro_begin(),
			wrapper.filtro_end());
	BOOST_CHECK(numero_domicilios == target_numero_domicilios);

	std::vector<std::string> str_domicilios;
	std::for_each(wrapper.filtro_begin(), wrapper.filtro_end(),
			[](Domicilio& domicilio) {
				domicilio.Informacion("Domicilio chequeado");});
	std::transform(wrapper.begin(), wrapper.end(),
			std::back_inserter(str_domicilios), [](const Domicilio& domicilio) {
				return domicilio.ToString();});

	BOOST_CHECK_EQUAL_COLLECTIONS(target_str_domicilios.begin(),
			target_str_domicilios.end(), str_domicilios.begin(),
			str_domicilios.end());
}
BOOST_AUTO_TEST_CASE( filtro_por_make_filter ) {

// Generamos los iteradores teniendo en cuenta el filtro
	auto it_begin = boost::make_filter_iterator(filtro, domicilios.begin(),
			domicilios.end());
	auto it_end = boost::make_filter_iterator(filtro, domicilios.end(),
			domicilios.end());
	BOOST_CHECK_EQUAL_COLLECTIONS(target_domicilios_filtrados.begin(),
			target_domicilios_filtrados.end(), it_begin, it_end);

	int numero_huespedes =
			std::accumulate(it_begin, it_end, 0,
					[](int acumulador,const Domicilio&domicilio) {return acumulador+domicilio.Huespedes();});
	BOOST_CHECK(numero_huespedes == target_numero_huespedes);

	int numero_domicilios = std::distance(it_begin, it_end);
	BOOST_CHECK(numero_domicilios == target_numero_domicilios);

	std::vector<std::string> str_domicilios;

	std::for_each(it_begin, it_end, [](Domicilio& domicilio) {
		domicilio.Informacion("Domicilio chequeado");});
	std::transform(domicilios.begin(), domicilios.end(),
			std::back_inserter(str_domicilios),
			std::mem_fn(&Domicilio::ToString));

	BOOST_CHECK_EQUAL_COLLECTIONS(target_str_domicilios.begin(),
			target_str_domicilios.end(), str_domicilios.begin(),
			str_domicilios.end());

}
BOOST_AUTO_TEST_CASE( filtro_por_rangos ) {

	std::vector<Domicilio> valores_filtrados;
	boost::copy(domicilios | boost::adaptors::filtered(filtro),
			std::back_inserter(valores_filtrados));
	BOOST_CHECK_EQUAL_COLLECTIONS(target_domicilios_filtrados.begin(),
			target_domicilios_filtrados.end(), valores_filtrados.begin(),
			valores_filtrados.end());

	int numero_huespedes =
			std::accumulate(valores_filtrados.begin(), valores_filtrados.end(),
					0,
					[](int acumulador,const Domicilio&domicilio) {return acumulador+domicilio.Huespedes();});
	BOOST_CHECK(numero_huespedes == target_numero_huespedes);

	int numero_domicilios = valores_filtrados.size();
	BOOST_CHECK(numero_domicilios == target_numero_domicilios);

	boost::for_each(domicilios | boost::adaptors::filtered(filtro),
			[](Domicilio& domicilio) {
				domicilio.Informacion("Domicilio chequeado");});

	std::vector<std::string> str_domicilios;
	boost::copy(
			domicilios
					| boost::adaptors::transformed(
							std::mem_fn(&Domicilio::ToString)),
			std::back_inserter(str_domicilios));

	BOOST_CHECK_EQUAL_COLLECTIONS(target_str_domicilios.begin(),
			target_str_domicilios.end(), str_domicilios.begin(),
			str_domicilios.end());

	std::cout << "CodigoPostalTest: " << codigo_postal_test
			<< ", Numero total de Huespedes: " << numero_huespedes
			<< ", Numero de domicilios: " << numero_domicilios << std::endl;

	std::cout
			<< boost::algorithm::join(
					domicilios
							| boost::adaptors::transformed(
									std::mem_fn(&Domicilio::ToString)), "\n");

}

BOOST_AUTO_TEST_SUITE_END()
