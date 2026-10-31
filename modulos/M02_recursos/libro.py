"""
Clase Libro — M02 (HERENCIA)

Representa un libro en el sistema.
Hereda de Recurso y agrega atributos específicos de libros.

Atributos heredados:
    - código, nombre, fecha_registro, estado, cantidad_prestamos

Atributos propios:
    - autor: Quién escribió el libro
    - isbn: Identificador internacional (para catalogación)
    - año_publicación: Cuándo se publicó

Ejemplo de herencia:
    class Recurso (padre):
        - código
        - nombre
        - estado
        - cantidad_prestamos
        + obtener_info()
        + es_disponible()
        + registrar_prestamo()

    class Libro (hijo, hereda de Recurso):
        + autor (nuevo)
        + isbn (nuevo)
        + año_publicación (nuevo)
        + obtener_info() (override: información del libro)
        + obtener_tipo() (override: retorna "Libro")
"""

from .recurso import Recurso


class Libro(Recurso):
    """
    Representa un libro en la biblioteca.

    Hereda de Recurso todos los métodos comunes.
    Agrega atributos específicos de libros.

    Atributos:
        codigo (str): Identificador único (heredado)
        nombre (str): Título del libro (heredado)
        autor (str): Autor del libro (NUEVO)
        isbn (str): ISBN (NUEVO)
        año_publicacion (int): Año de publicación (NUEVO)
        estado (str): "Disponible"/"No disponible"/"Dado de baja" (heredado)
        cantidad_prestamos (int): Cuántas veces se prestó (heredado)

    Métodos:
        __init__: Constructor
        obtener_tipo: "Libro" (override)
        obtener_info: Información completa (override)
        __str__: Representación

    Ejemplo de uso:
        >>> libro = Libro("R001", "Clean Code", "Robert Martin", "978-0132350884", 2008)
        >>> print(libro.obtener_tipo())
        'Libro'
        >>> print(libro.autor)
        'Robert Martin'
        >>> print(libro.es_disponible())
        True
        >>> libro.registrar_prestamo()
        >>> print(libro.cantidad_prestamos)
        1
        >>> info = libro.obtener_info()
        >>> print(info['isbn'])
        '978-0132350884'
    """

    def __init__(self, codigo, nombre, autor, isbn, año_publicacion):
        """
        Crea un libro.

        Args:
            codigo (str): Identificador único (ej: "R001")
            nombre (str): Título del libro
            autor (str): Nombre del autor
            isbn (str): ISBN del libro
            año_publicacion (int): Año de publicación

        Ejemplo:
            >>> libro = Libro("R001", "Python Cookbook", "David Beazley", "978-1449357337", 2013)
            >>> print(libro.codigo)
            'R001'
            >>> print(libro.autor)
            'David Beazley'
        """
        # Llamar al constructor de la clase padre
        super().__init__(codigo, nombre)

        # Atributos específicos del libro
        self.autor = autor
        self.isbn = isbn
        self.año_publicacion = año_publicacion

    def obtener_tipo(self):
        """
        Retorna el tipo de recurso.

        Returns:
            str: "Libro"

        Ejemplo:
            >>> libro = Libro("R001", "Python", "Guido", "978-123", 2000)
            >>> libro.obtener_tipo()
            'Libro'
        """
        return "Libro"

    def obtener_info(self):
        """
        Retorna información completa del libro.

        Override del método abstract de Recurso.
        Incluye tanto atributos heredados como propios.

        Returns:
            dict: Información del libro

        Ejemplo:
            >>> libro = Libro("R001", "Python", "Guido", "978-123", 2000)
            >>> info = libro.obtener_info()
            >>> print(info['tipo'])
            'Libro'
            >>> print(info['autor'])
            'Guido'
            >>> print(info['estado'])
            'Disponible'
        """
        return {
            'codigo': self.codigo,
            'tipo': self.obtener_tipo(),
            'nombre': self.nombre,
            'autor': self.autor,
            'isbn': self.isbn,
            'año_publicacion': self.año_publicacion,
            'estado': self.estado,
            'cantidad_prestamos': self.cantidad_prestamos,
            'fecha_registro': self.fecha_registro.strftime("%Y-%m-%d"),
            'disponible': self.es_disponible(),
        }

    def obtener_autor(self):
        """Obtiene el autor del libro."""
        return self.autor

    def obtener_isbn(self):
        """Obtiene el ISBN del libro."""
        return self.isbn

    def obtener_año(self):
        """Obtiene el año de publicación."""
        return self.año_publicacion

    def __str__(self):
        """Representación legible."""
        return f"Libro({self.codigo}: '{self.nombre}' by {self.autor}, ISBN {self.isbn}, {self.estado})"

    def __repr__(self):
        """Para debug."""
        return f"Libro(codigo='{self.codigo}', nombre='{self.nombre}', autor='{self.autor}', isbn='{self.isbn}', año={self.año_publicacion})"
