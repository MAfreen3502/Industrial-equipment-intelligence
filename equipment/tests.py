from django.test import TestCase
from equipment.models import Equipment
from django.db import IntegrityError, transaction


class EquipmentModelTests(TestCase):

    def test_equipment_creation(self):

        equipment = Equipment.objects.create(
            engine_id=101
        )

        self.assertEqual(equipment.engine_id, 101)

        self.assertEqual(Equipment.objects.count(), 1)

        self.assertEqual(str(equipment), "Engine 101")

    def test_equipment_default_values(self):

        equipment = Equipment.objects.create(
            engine_id=102
        )

        self.assertEqual(
            equipment.equipment_type,
            'Simulated Turbofan Engine'
        )

        self.assertEqual(
            equipment.dataset,
            'NASA C-MAPSS FD001'
        )


    def test_duplicate_engine_id_is_rejected(self):

        Equipment.objects.create(engine_id=103)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Equipment.objects.create(engine_id=103)
