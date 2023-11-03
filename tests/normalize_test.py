import unittest
from core.relation import Relation
from core.attribute import Attribute
from core.dependency import Dependency
from application.normalize import *
from application.relation_helper_functions import *

class Normalize_Test(unittest.TestCase):
    def test_split_a_relation(self):
        # Arrange
        # Split R(Course, Professor, ProfessorEmail, CourseStart, CourseEnd) into R(Course, Professor, CourseStart, CourseEnd) and S(Professor, ProfessorEmail)
        test_attributes = [
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Professor", data_type="varchar(50)", isAtomic=True),
            Attribute(name="ProfessorEmail", data_type="varchar(50)", isAtomic=True),
            Attribute(name="CourseStart", data_type="date", isAtomic=True),
            Attribute(name="CourseEnd", data_type="date", isAtomic=True)
        ]
        test_tuples = [
            ["Math101","Dr.Smith","smith@mst.edu","1/1/2023","5/30/2023"],
            ["CS101","Dr.Jones","jones@mst.edu","2/1/2023","6/15/2023"],
            ["Bio101","Dr.Watson","watson@mst.edu","3/1/2023","7/20/2023"]
        ]
        test_primary_keys = [
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True)
        ]
        test_dependencies = [
            Dependency(parent="Course", children=["CourseStart","CourseEnd"]),
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
        (actual_staying, actual_going) = split_tuples(test_relation, split_relation_key="Professor", split_relation_attributes=["ProfessorEmail"])

        # Assert
        expected_staying = [
            ["Math101","Dr.Smith","1/1/2023","5/30/2023"],
            ["CS101","Dr.Jones","2/1/2023","6/15/2023"],
            ["Bio101","Dr.Watson","3/1/2023","7/20/2023"]
        ]
        expected_going = [
            ["Dr.Smith","smith@mst.edu"],
            ["Dr.Jones","jones@mst.edu"],
            ["Dr.Watson","watson@mst.edu"]
        ]

        self.assertEqual(expected_staying, actual_staying)
        self.assertEqual(expected_going, actual_going)

    def test_given_UNF_Normalize_to_1NF(self):
        # Arrange
        test_attributes = [
            Attribute(name="StudentID", data_type="int", isAtomic=True),
            Attribute(name="FirstName", data_type="varchar(50)", isAtomic=True),
            Attribute(name="LastName", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Professor", data_type="varchar(50)", isAtomic=True),
            Attribute(name="ProfessorEmail", data_type="varchar(50)", isAtomic=True),
            Attribute(name="CourseStart", data_type="date", isAtomic=True),
            Attribute(name="CourseEnd", data_type="date", isAtomic=False)
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
        actual = normalize_to_1NF(test_relation)[0]

        # Assert
        self.assertTrue(areRelationsEquivalent(test_relation, actual))
    def test_given_1NF_Normalize_to_2NF(self):
        # Arrange
        test_attributes = [
            Attribute(name="StudentID", data_type="int", isAtomic=True),
            Attribute(name="FirstName", data_type="varchar(50)", isAtomic=True),
            Attribute(name="LastName", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Professor", data_type="varchar(50)", isAtomic=True),
            Attribute(name="ProfessorEmail", data_type="varchar(50)", isAtomic=True),
            Attribute(name="CourseStart", data_type="date", isAtomic=True),
            Attribute(name="CourseEnd", data_type="date", isAtomic=True)
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
        self.assertEqual(3, len(actual))
        for relation in actual:
            self.assertTrue(isRelationIn2NF(relation))

if __name__ == '__main__':
    unittest.main()
