from setups_for_tests import *
import pymongo


@with_local_database
def test_can_insert_one(cli: pymongo.MongoClient):
    # Try to insert a simple doc
    assert cli.xs.abcdef.count_documents({}) == 0

    test_id = cli.xs.abcdef.insert_one({"hello": "world"}).inserted_id
    assert cli.xs.abcdef.count_documents({}) == 1

    # Find it again in the db. This should be the only document.
    test_doc = cli.xs.abcdef.find_one()

    assert test_doc["_id"] == test_id
    assert test_doc["hello"] == "world"


@with_local_database
def test_can_remove_single_by_id(cli: pymongo.MongoClient):
    # Insert some docs
    test_id_1 = cli.xs.abcdef.insert_one({"will_be_deleted": "yes"}).inserted_id
    test_id_2 = cli.xs.abcdef.insert_one({"will_be_deleted": "no"}).inserted_id
    assert cli.xs.abcdef.count_documents({}) == 2

    # Remove the first one
    cli.xs.abcdef.find_one_and_delete({"_id": test_id_1})
    assert cli.xs.abcdef.count_documents({}) == 1

    # Find the remaining one
    left = cli.xs.abcdef.find_one()
    assert left["_id"] == test_id_2
    assert left["will_be_deleted"] == "no"
