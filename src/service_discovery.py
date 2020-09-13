import inspect
import os
import pkgutil
from iplugin import IPlugin

class ServiceDiscovery(object):
    """Upon creation, this class will read the plugins package for modules
    that contain a class definition that is inheriting from the Plugin class
    """

    def __init__(self, plugin_package_dir='plugins'):
        """Constructor that initiates the reading of all available plugins
        when an instance of the PluginCollection object is created
        """
        self.plugin_package_base_dir = plugin_package_dir
        self.plugin_topic_instance_map = {}

        self.reload_plugins()

    def execute(self, topic, argument):
        if topic not in self.plugin_topic_instance_map:
            raise Exception (f'Topic: {topic} is not registered')

        return self.plugin_topic_instance_map[topic].execute(topic, argument)

    def reload_plugins(self):
        """Reset the list of all plugins and initiate the walk over the main
        provided plugin package to load all available plugins
        """
        self.seen_paths = []
        print(f'Looking for plugins under package {self.plugin_package_base_dir}')
        self.enumerate_packages(self.plugin_package_base_dir)

    def enumerate_packages(self, package):
        """Recursively walk the supplied package to retrieve all plugins
        """
        imported_package = __import__(package, fromlist=['foo'])

        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                plugin_module = __import__(pluginname, fromlist=['foo'])
                clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in clsmembers:
                    # Only add classes that are a sub class of Plugin, but NOT Plugin itself
                    if issubclass(c, IPlugin) & (c is not IPlugin):
                        print(f'    Found plugin class: {c.__module__}.{c.__name__}')
                        cls_instance = c()
                        for topic in cls_instance.topics:
                            print(f'        Registering Topics: {topic}')
                            self.plugin_topic_instance_map[topic] = cls_instance

        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # Get all sub directory of the current package path directory
                child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]

                # For each sub directory, apply the walk_package method recursively
                for child_pkg in child_pkgs:
                    self.enumerate_packages(package + '.' + child_pkg)
