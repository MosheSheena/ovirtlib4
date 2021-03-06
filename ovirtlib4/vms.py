# -*- coding: utf-8 -*-

from .system_service import CollectionService, CollectionEntity
import ovirtsdk4.types as types
from . import defaults, disks, hosts


class Vms(CollectionService):
    """
    Gives access to all Ovirt VMs
    """
    @property
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.system_service().vms_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service.vm_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.Vm

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmEntity(connection=self.connection)

    def get_vms(self, he_name=defaults.HOSTED_ENGINE_VM_NAME):
        """ Return all VMs beside the HostedEngine VM """
        return self.list(search="name!={name}".format(name=he_name))

    def get_hosted_engine_vm(self, he_name=defaults.HOSTED_ENGINE_VM_NAME):
        """ Return the hosted-engine VM: (VmEntity) """
        vms = self.list(search="name={name}".format(name=he_name))
        if vms:
            return vms[0]
        return None

    def get_hosted_engine_host(self):
        """
        Return the host Entity of the HostedEngine VM, or None if not found
        """
        vm = self.get_hosted_engine_vm()
        if vm:
            host_id = vm.entity.host.id
            if host_id:
                return hosts.Hosts(self.connection).get_entity_by_id(id=host_id)
        return None


class VmEntity(CollectionEntity):
    """
    Put VM custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)

    def get_disk_attachments(self):
        """ Return list of all VM disks: [CollectionEntity] """
        return self.follow_link(
            collection_service=disks.Disks(self.connection),
            link=self.entity.disk_attachments
        )

    @property
    def nics(self):
        return VmNics(connection=self.service)

    @property
    def disks(self):
        return VmDisks(connection=self.service)


class VmNics(CollectionService):
    """
    Gives access to all VM NICs
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.nics_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().nic_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.Nic

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmNic(connection=self.connection)


class VmNic(CollectionEntity):
    """
    Put VmNic custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)


class VmDisks(CollectionService):
    """
    Gives access to all VM attached disks
    """
    def service(self):
        """ Overwrite abstract parent method """
        return self.connection.disk_attachments_service()

    def _entity_service(self, id):
        """ Overwrite abstract parent method """
        return self.service().attachment_service(id=id)

    def entity_type(self):
        """ Overwrite abstract parent method """
        return types.DiskAttachment

    def _get_collection_entity(self):
        """ Overwrite abstract parent method """
        return VmDisk(connection=self.connection)


class VmDisk(CollectionEntity):
    """
    Put VmDisk custom functions here
    """
    def __init__(self, *args, **kwargs):
        CollectionEntity. __init__(self, *args, **kwargs)
