<?php
if (!defined('BASEPATH'))
    exit('No direct script access allowed');
session_start();

class Vehicle_tracking extends CI_Controller
{

    function __construct(){
        parent::__construct();
        $this->load->model('students');

    }

    function index(){
        $this->load->view('tracking/map');

    }

    function login_message(){
        $this->load->view('tracking/modals/login_message');
    }

    function spatial_object_info($id){
        $this->load->view('tracking/modals/spatial_object_info',array('id'=>$id));
    }

    function today($id){
        $this->load->view('tracking/modals/spatial_object_info',array('id'=>$id));
    }

    function bigdata(){

        $data_stats = $this->students->stats();
//        $this->load->view('bigdata/index',array('data_stats' => $data_stats));
////        $this->output->set_content_type('application/json');
        var_dump($data_stats);
    }

    function all_students(){
        $data_stats = $this->students->all();
        $this -> output -> set_content_type('application/json') -> set_output(json_encode($data_stats));
    }


    function get_student($reg_number){
        $student = $this->students->get($reg_number);
        $this->output->set_content_type('application/json') -> set_output(json_encode($student));
    }

}
