<?php

class Students extends CI_Model
{

    function __construct()
    {
        // Call the Model constructor
        parent::__construct();
        $this->mongodb = new MongoClient();
        $this->uni_db = $this->mongodb->uni;
    }

    function stats(){
        $collection_stats = $this->uni_db->command(array('collStats' => 'students'));
        return $collection_stats;
    }

    function all(){
        $cursor = $this->uni_db->students->find(array('location' => array('$exists' => true )) ,array('reg_number' => 1, '_id'=> false, 'name' => 1, 'location.location' => 1));
        /*db.history.find({id: 14,'properties.timeStamp': {"$lte": Date()}}).count()*/
        $data= array();
        foreach ($cursor as $doc) {
            $data[]= $doc;
        }

        return $data;
    }

    function get($reg_number){
        $student = $this->uni_db->students->findOne(array('reg_number' => $reg_number));
        return $student;
    }

}
