/*
 * Domicilio.cpp
 *
 *  Created on: Nov 20, 2016
 *      Author: pedro
 */

#include "../include/Domicilio.h"
#include <sstream>

using namespace IteradoresPersonalizados;

int Domicilio::numero_domicilios_totales = 0;

Domicilio::Domicilio(int codigo_postal, int huespedes, std::string informacion) :
		codigo_postal(codigo_postal), huespedes(huespedes), informacion(
				informacion), id(numero_domicilios_totales++) {

}

int Domicilio::CodigoPostal() const {
	return codigo_postal;
}

int Domicilio::Huespedes() const {
	return huespedes;
}

void Domicilio::Informacion(const std::string &informacion) {
	this->informacion = informacion;
}

std::string Domicilio::Informacion() const {
	return informacion;
}

std::string Domicilio::ToString() const {
	std::ostringstream buffer;
	buffer << "CodigoPostal: " << codigo_postal << ", Huespedes: " << huespedes
			<< ", ID: " << id<<", Informacion: "<<informacion;
	return buffer.str();
}

std::vector<Domicilio> Domicilio::DomiciliosRandom(size_t numero_de_domicilios,
		int codigo_postal_inicial, int codigo_postal_final) {
	// Generamos los codigos postales y huespedes con una distribucion uniforme
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_int_distribution<> dis_cp(codigo_postal_inicial,
			codigo_postal_final);
	std::uniform_int_distribution<> dis_huespedes(0, 5);

	std::vector<Domicilio> domicilios;
	std::generate_n(std::back_inserter(domicilios), numero_de_domicilios,
			[&]() {return Domicilio(dis_cp(gen),dis_huespedes(gen));});
	return domicilios;
}

bool Domicilio::operator!=(const Domicilio& rhs) {
	return this->id != rhs.id;
}

std::ostream& IteradoresPersonalizados::operator<<(std::ostream& out,
		const Domicilio& f) {
	return out << f.ToString();
}

