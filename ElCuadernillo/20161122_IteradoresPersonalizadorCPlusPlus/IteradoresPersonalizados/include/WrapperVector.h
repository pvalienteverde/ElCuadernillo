/*
 * WrapperVector.h
 *
 *  Created on: Nov 9, 2016
 *      Author: pedro valiente verde
 */

#ifndef SRC_WRAPPERVECTOR_H_
#define SRC_WRAPPERVECTOR_H_

#include <vector>
#include <functional>
#include <boost/iterator/filter_iterator.hpp>

namespace IteradoresPersonalizados {

/**
 * Clase que envuelve a std::vector, añadiendo un iterador en base
 * al predicado especifico
 */
template<typename T>
class WrapperVector: public std::vector<T> {
public:
	typedef std::vector<T> Vector;
	typedef std::function<bool(T)> Filtro;
	typedef boost::filter_iterator<Filtro, typename Vector::iterator> IteradorFiltro;

	WrapperVector(const Vector &valores, Filtro filtro) :
			Vector(valores), filtro(filtro) {
	}

	IteradorFiltro filtro_begin() {
		return IteradorFiltro(filtro, Vector::begin(), Vector::end());
	}

	IteradorFiltro filtro_end() {
		return IteradorFiltro(filtro, Vector::end(), Vector::end());
	}

private:
	Filtro filtro;
};
}

#endif /* SRC_WRAPPERVECTOR_H_ */

