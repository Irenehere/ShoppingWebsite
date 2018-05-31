<?php
class Login{
	private $user;
	private $passwd;
	public function __construct($user, $passwd){
		$this->user = $user;
		$this->passwd = $passwd;
	}
	public function check(){
		if ($_POST['user']=='c201804281547' && $_POST['passwd']=='123456'){
			return true;
		} else {
			return false;
		}
	}
}