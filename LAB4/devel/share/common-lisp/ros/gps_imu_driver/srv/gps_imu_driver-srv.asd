
(cl:in-package :asdf)

(defsystem "gps_imu_driver-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "convert_to_quaternion" :depends-on ("_package_convert_to_quaternion"))
    (:file "_package_convert_to_quaternion" :depends-on ("_package"))
  ))