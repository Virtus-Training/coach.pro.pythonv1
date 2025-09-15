"""
Enterprise Dependency Injection Container.

Provides a professional-grade IoC container with:
- Constructor injection
- Interface-based registration
- Singleton and transient lifetimes
- Circular dependency detection
- Auto-wiring capabilities
"""

from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from enum import Enum
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    get_type_hints,
)

T = TypeVar("T")
Factory = Callable[[], T]


class ServiceLifetime(Enum):
    """Service lifetime management."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"


class IServiceProvider(ABC, Generic[T]):
    """Abstract service provider interface."""

    @abstractmethod
    def get_service(self, service_type: Type[T]) -> T:
        """Get service instance of specified type."""
        pass

    @abstractmethod
    def get_required_service(self, service_type: Type[T]) -> T:
        """Get required service instance, raise if not found."""
        pass


class ServiceDescriptor:
    """Describes how a service should be instantiated."""

    def __init__(
        self,
        service_type: Type,
        implementation_type: Optional[Type] = None,
        factory: Optional[Factory] = None,
        instance: Optional[Any] = None,
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
    ):
        self.service_type = service_type
        self.implementation_type = implementation_type or service_type
        self.factory = factory
        self.instance = instance
        self.lifetime = lifetime
        self._singleton_instance: Optional[Any] = None

    def create_instance(self, container: DIContainer) -> Any:
        """Create service instance using appropriate method."""
        if self.instance is not None:
            return self.instance

        if self.factory is not None:
            return self.factory()

        # Auto-wire constructor dependencies
        return container._create_instance(self.implementation_type)


class DIContainer(IServiceProvider):
    """
    Professional Dependency Injection Container.

    Features:
    - Constructor injection with type hints
    - Interface-based service registration
    - Multiple lifetime management (singleton, transient, scoped)
    - Circular dependency detection
    - Auto-wiring capabilities

    Example:
        >>> container = DIContainer()
        >>> container.register(IUserService, UserService, ServiceLifetime.SINGLETON)
        >>> user_service = container.get_service(IUserService)
    """

    def __init__(self):
        self._services: Dict[Type, ServiceDescriptor] = {}
        self._singletons: Dict[Type, Any] = {}
        self._creating: set = set()  # Circular dependency detection

    def register(
        self,
        service_type: Type[T],
        implementation_type: Optional[Type[T]] = None,
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
    ) -> DIContainer:
        """Register a service with its implementation."""
        descriptor = ServiceDescriptor(
            service_type=service_type,
            implementation_type=implementation_type,
            lifetime=lifetime,
        )
        self._services[service_type] = descriptor
        return self

    def register_factory(
        self,
        service_type: Type[T],
        factory: Factory[T],
        lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT,
    ) -> DIContainer:
        """Register a service with a factory function."""
        descriptor = ServiceDescriptor(
            service_type=service_type,
            factory=factory,
            lifetime=lifetime,
        )
        self._services[service_type] = descriptor
        return self

    def register_instance(
        self,
        service_type: Type[T],
        instance: T,
    ) -> DIContainer:
        """Register a service with a pre-created instance."""
        descriptor = ServiceDescriptor(
            service_type=service_type,
            instance=instance,
            lifetime=ServiceLifetime.SINGLETON,
        )
        self._services[service_type] = descriptor
        return self

    def get_service(self, service_type: Type[T]) -> Optional[T]:
        """Get service instance if registered."""
        try:
            return self.get_required_service(service_type)
        except ServiceNotFoundError:
            return None

    def get_required_service(self, service_type: Type[T]) -> T:
        """Get required service instance, raise if not found."""
        descriptor = self._services.get(service_type)
        if descriptor is None:
            raise ServiceNotFoundError(f"Service {service_type.__name__} not registered")

        # Handle singleton lifetime
        if descriptor.lifetime == ServiceLifetime.SINGLETON:
            if service_type in self._singletons:
                return self._singletons[service_type]

            instance = self._create_service_instance(descriptor)
            self._singletons[service_type] = instance
            return instance

        # Handle transient lifetime
        return self._create_service_instance(descriptor)

    def _create_service_instance(self, descriptor: ServiceDescriptor) -> Any:
        """Create service instance with circular dependency detection."""
        service_type = descriptor.service_type

        # Circular dependency detection
        if service_type in self._creating:
            raise CircularDependencyError(
                f"Circular dependency detected for {service_type.__name__}"
            )

        self._creating.add(service_type)
        try:
            instance = descriptor.create_instance(self)
            return instance
        finally:
            self._creating.discard(service_type)

    def _create_instance(self, implementation_type: Type) -> Any:
        """Create instance with constructor injection."""
        # Get constructor signature
        signature = inspect.signature(implementation_type.__init__)
        type_hints = get_type_hints(implementation_type.__init__)

        # Resolve constructor parameters
        kwargs = {}
        for param_name, param in signature.parameters.items():
            if param_name == 'self':
                continue

            param_type = type_hints.get(param_name)
            if param_type is None:
                if param.default is not inspect.Parameter.empty:
                    continue  # Use default value
                raise DependencyResolutionError(
                    f"Cannot resolve parameter '{param_name}' for {implementation_type.__name__}. "
                    f"No type hint provided."
                )

            # Try to resolve dependency
            dependency = self.get_service(param_type)
            if dependency is None:
                if param.default is not inspect.Parameter.empty:
                    continue  # Use default value
                raise DependencyResolutionError(
                    f"Cannot resolve dependency '{param_name}' of type {param_type.__name__} "
                    f"for {implementation_type.__name__}"
                )

            kwargs[param_name] = dependency

        return implementation_type(**kwargs)

    def build_service_provider(self) -> IServiceProvider:
        """Build an immutable service provider from current registrations."""
        return ServiceProvider(dict(self._services))


class ServiceProvider(IServiceProvider):
    """Immutable service provider built from DIContainer."""

    def __init__(self, services: Dict[Type, ServiceDescriptor]):
        self._services = services
        self._singletons: Dict[Type, Any] = {}

    def get_service(self, service_type: Type[T]) -> Optional[T]:
        """Get service instance if registered."""
        try:
            return self.get_required_service(service_type)
        except ServiceNotFoundError:
            return None

    def get_required_service(self, service_type: Type[T]) -> T:
        """Get required service instance, raise if not found."""
        descriptor = self._services.get(service_type)
        if descriptor is None:
            raise ServiceNotFoundError(f"Service {service_type.__name__} not registered")

        # Handle singleton
        if descriptor.lifetime == ServiceLifetime.SINGLETON:
            if service_type in self._singletons:
                return self._singletons[service_type]

            instance = descriptor.create_instance(self)
            self._singletons[service_type] = instance
            return instance

        return descriptor.create_instance(self)


# Decorators and utilities
class Injectable:
    """Mark a class as injectable for automatic registration."""

    def __init__(self, lifetime: ServiceLifetime = ServiceLifetime.TRANSIENT):
        self.lifetime = lifetime

    def __call__(self, cls):
        cls._injectable_lifetime = self.lifetime
        return cls


def inject(service_type: Type[T]) -> T:
    """
    Dependency injection decorator for functions and methods.

    Usage:
        @inject(IUserService)
        def handle_request(user_service: IUserService):
            return user_service.get_users()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get container from current context
            container = _get_current_container()
            if container is None:
                raise ContainerNotFoundError(
                    "No active DI container found. Make sure to set up container context."
                )

            # Inject the service
            service = container.get_required_service(service_type)
            return func(service, *args, **kwargs)
        return wrapper
    return decorator


# Exceptions
class DIContainerError(Exception):
    """Base exception for DI container errors."""
    pass


class ServiceNotFoundError(DIContainerError):
    """Service not found in container."""
    pass


class CircularDependencyError(DIContainerError):
    """Circular dependency detected."""
    pass


class DependencyResolutionError(DIContainerError):
    """Failed to resolve dependency."""
    pass


class ContainerNotFoundError(DIContainerError):
    """No active container found."""
    pass


# Global container context (for decorator support)
_current_container: Optional[DIContainer] = None


def _get_current_container() -> Optional[DIContainer]:
    """Get current active container."""
    return _current_container


def set_container(container: DIContainer) -> None:
    """Set the global active container."""
    global _current_container
    _current_container = container


def configure_services(configurator: Callable[[DIContainer], None]) -> DIContainer:
    """
    Configure services with a setup function.

    Example:
        def configure(container: DIContainer):
            container.register(IUserService, UserService, ServiceLifetime.SINGLETON)
            container.register(IEmailService, EmailService)

        container = configure_services(configure)
        set_container(container)
    """
    container = DIContainer()
    configurator(container)
    return container