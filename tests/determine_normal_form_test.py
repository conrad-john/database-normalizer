import unittest
from core.relation import Relation
from core.attribute import Attribute
from core.dependency import Dependency
from application.normalize import *
from application.relation_helper_functions import *

class Determine_Normal_Form_Test(unittest.TestCase):
    def test_given_non_atomic_UNF_returns_UNF(self):
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
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("UNF", actual)
    def test_given_no_key_UNF_returns_UNF(self):
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
        test_primary_keys = []
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
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("UNF", actual)
    def test_given_inconsistent_data_type_UNF_returns_UNF(self):
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
            ["105","Ada","Lovelace","CS101","Dr.Jones","jones@mst.edu","2/1/2023","potato"]
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
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("UNF", actual)
    def test_given_1NF_returns_not_UNF(self):
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
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertNotEqual("UNF", actual)
    def test_given_partial_dependency_1NF_returns_1NF(self):
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
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("1NF", actual)
    def test_given_partial_dependency_partial_name_match_1NF_returns_1NF(self):
        # Arrange
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
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Professor", data_type="varchar(50)", isAtomic=True)
        ]
        test_dependencies = [
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
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("1NF", actual)
    def test_given_partial_dependency_partial_name_match_2NF_returns_2NF(self):
        # Arrange
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
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Professor", data_type="varchar(50)", isAtomic=True)
        ]
        test_dependencies = [
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
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("1NF", actual)
    def test_given_transitive_dependency_2NF_returns_2NF(self):
        # Arrange
        # Course* -> Professor -> ProfessorEmail
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
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("2NF", actual)
    def test_given_non_key_dependency_3NF_returns_3NF(self):
        # Arrange
        # Course* -> CourseStart, CourseEnd
        # Professor -> ProfessorEmail
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
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("3NF", actual)
    def test_given_multi_value_dependency_BCNF_returns_BCNF(self):
        # Arrange
        # Course* -> CourseStart, CourseEnd
        # Course* ->-> Professor
        test_attributes = [
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Professor", data_type="varchar(50)", isAtomic=True),
            Attribute(name="CourseStart", data_type="date", isAtomic=True),
            Attribute(name="CourseEnd", data_type="date", isAtomic=True)
        ]
        test_tuples = [
            ["Math101","Dr.Smith","3/1/2023","5/30/2023"],
            ["Math101","Dr.Jones","3/1/2023","5/30/2023"],
            ["Math101","Dr.Watson","3/1/2023","5/30/2023"]
        ]
        test_primary_keys = [
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True)
        ]
        test_dependencies = [
            Dependency(parent="Course", children=["CourseStart","CourseEnd","Professor"])
        ]
        test_relation= Relation(
            name="test_relation",
            attributes=test_attributes,
            tuples=test_tuples,
            primary_keys=test_primary_keys,
            dependencies=test_dependencies
        )
        # Act
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("BCNF", actual)
    def test_given_join_dependency_4NF_returns_4NF(self):
        # Arrange
        # Course* -> CourseStart, CourseEnd
        # Professor*
        test_attributes = [
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="Professor", data_type="varchar(50)", isAtomic=True),
            Attribute(name="CourseStart", data_type="date", isAtomic=True),
            Attribute(name="CourseEnd", data_type="date", isAtomic=True)
        ]
        test_tuples = [
            ["Math101","Dr.Smith","3/1/2023","5/30/2023"],
            ["Math101","Dr.Jones","3/1/2023","5/30/2023"],
            ["Math101","Dr.Watson","3/1/2023","5/30/2023"]
        ]
        test_primary_keys = [
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True)
        ]
        test_dependencies = [
            Dependency(parent="Course", children=["CourseStart","CourseEnd"])
        ]
        test_relation= Relation(
            name="test_relation",
            attributes=test_attributes,
            tuples=test_tuples,
            primary_keys=test_primary_keys,
            dependencies=test_dependencies
        )
        # Act
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("4NF", actual)
    def test_given_5NF_returns_5NF(self):
        # Arrange
        # Course* -> CourseStart, CourseEnd
        test_attributes = [
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True),
            Attribute(name="CourseStart", data_type="date", isAtomic=True),
            Attribute(name="CourseEnd", data_type="date", isAtomic=True)
        ]
        test_tuples = [
            ["Math101","3/1/2023","5/30/2023"],
            ["CompSci201","3/1/2023","5/30/2023"]
        ]
        test_primary_keys = [
            Attribute(name="Course", data_type="varchar(50)", isAtomic=True)
        ]
        test_dependencies = [
            Dependency(parent="Course", children=["CourseStart","CourseEnd"])
        ]
        test_relation= Relation(
            name="test_relation",
            attributes=test_attributes,
            tuples=test_tuples,
            primary_keys=test_primary_keys,
            dependencies=test_dependencies
        )
        # Act
        actual = determine_normal_form(test_relation)
        # Assert
        self.assertEqual("4NF", actual)
if __name__ == '__main__':
    unittest.main()
