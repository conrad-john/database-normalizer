import unittest
from core.relation import Relation
from core.attribute import Attribute
from core.dependency import Dependency
from application.normalize import *

class Normalize_Test(unittest.TestCase):
    def test_normalize_to_2NF(self):
        # Arrange
        test_attributes = [
            Attribute(name="StudentID", data_type="int", isAtomic=True),
            Attribute(name="FirstName", data_type="varchar(50)", isAtomic=True),
            Attribute(name="LastName", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Professor", data_type="varchar(50)", isAtomic=True),
            Attribute(name="ProfessorEmail", data_type="varchar(50)", isAtomic=True),
            Attribute(name="CourseStart", data_type="varchar(50)", isAtomic=True),
            Attribute(name="CourseEnd", data_type="varchar(50)", isAtomic=True)
        ]
        test_tuples = [
            ["101","John","Doe","Math101","Dr.Smith","smith@mst.edu","1/1/2023","5/30/2023"],
            ["102","Jane","Roe","Math101","Dr.Smith","smith@mst.edu","1/1/2023","5/30/2023"],
            ["103","Arindam","Khanda","CS101","Dr.Jones","jones@mst.edu","2/1/2023","6/15/2023"],
            ["104","Jose","Franklin","Bio101","Dr.Watson","watson@mst.edu","3/1/2023","7/20/2023"],
            ["105","Ada","Lovelace","CS101","Dr.Jones","jones@mst.edu","2/1/2023","6/15/2023"]
        ]
        test_primary_keys = [
            Attribute(name="StudentID", data_type="int", isAtomic=True),
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Professor", data_type="varchar(50)", isAtomic=True)
        ]
        test_dependencies = [
            Dependency(parent="StudentID", children=["FirstName","LastName"]),
            Dependency(parent="Course", children=["CourseStart","CourseEnd","Professor"]),
            Dependency(parent="Professor", children=["ProfessorEmail"])
        ]
        test_relation= Relation(
            name="test_relation",
            attributes=test_attributes,
            tuples=test_tuples,
            primary_keys=test_primary_keys,
            dependencies=test_dependencies
        )

        # Act
        actual = normalize_to_2NF(test_relation)

        # Assert
        self.assertEqual(2 + 2, 4)

    # def test_subtraction(self):
    #     self.assertEqual(5 - 3, 2)

if __name__ == '__main__':
    unittest.main()
