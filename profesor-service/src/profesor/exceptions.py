class BusinessError(Exception):
    """
    Se lanza cuando se viola una regla de negocio.
    Ejemplo: intentar crear un profesor con email ya registrado.
    El router la convierte en HTTP 409 Conflict.
    """


class ResourceNotFoundError(Exception):
    """
    Se lanza cuando no se encuentra el recurso solicitado.
    Ejemplo: buscar un profesor con id que no existe.
    El router la convierte en HTTP 404 Not Found.
    """
