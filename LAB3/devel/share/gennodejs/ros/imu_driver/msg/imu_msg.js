// Auto-generated. Do not edit!

// (in-package imu_driver.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');
let sensor_msgs = _finder('sensor_msgs');

//-----------------------------------------------------------

class imu_msg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.Header = null;
      this.IMU = null;
      this.MagField = null;
      this.IMU_backup = null;
    }
    else {
      if (initObj.hasOwnProperty('Header')) {
        this.Header = initObj.Header
      }
      else {
        this.Header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('IMU')) {
        this.IMU = initObj.IMU
      }
      else {
        this.IMU = new sensor_msgs.msg.Imu();
      }
      if (initObj.hasOwnProperty('MagField')) {
        this.MagField = initObj.MagField
      }
      else {
        this.MagField = new sensor_msgs.msg.MagneticField();
      }
      if (initObj.hasOwnProperty('IMU_backup')) {
        this.IMU_backup = initObj.IMU_backup
      }
      else {
        this.IMU_backup = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type imu_msg
    // Serialize message field [Header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.Header, buffer, bufferOffset);
    // Serialize message field [IMU]
    bufferOffset = sensor_msgs.msg.Imu.serialize(obj.IMU, buffer, bufferOffset);
    // Serialize message field [MagField]
    bufferOffset = sensor_msgs.msg.MagneticField.serialize(obj.MagField, buffer, bufferOffset);
    // Serialize message field [IMU_backup]
    bufferOffset = _serializer.string(obj.IMU_backup, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type imu_msg
    let len;
    let data = new imu_msg(null);
    // Deserialize message field [Header]
    data.Header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [IMU]
    data.IMU = sensor_msgs.msg.Imu.deserialize(buffer, bufferOffset);
    // Deserialize message field [MagField]
    data.MagField = sensor_msgs.msg.MagneticField.deserialize(buffer, bufferOffset);
    // Deserialize message field [IMU_backup]
    data.IMU_backup = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.Header);
    length += sensor_msgs.msg.Imu.getMessageSize(object.IMU);
    length += sensor_msgs.msg.MagneticField.getMessageSize(object.MagField);
    length += _getByteLength(object.IMU_backup);
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'imu_driver/imu_msg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '00ccca0a92f0ac88045addd61ca8c562';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    std_msgs/Header Header
    sensor_msgs/Imu IMU
    sensor_msgs/MagneticField MagField
    string IMU_backup
    
    ================================================================================
    MSG: std_msgs/Header
    # Standard metadata for higher-level stamped data types.
    # This is generally used to communicate timestamped data 
    # in a particular coordinate frame.
    # 
    # sequence ID: consecutively increasing ID 
    uint32 seq
    #Two-integer timestamp that is expressed as:
    # * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
    # * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
    # time-handling sugar is provided by the client library
    time stamp
    #Frame this data is associated with
    string frame_id
    
    ================================================================================
    MSG: sensor_msgs/Imu
    # This is a message to hold data from an IMU (Inertial Measurement Unit)
    #
    # Accelerations should be in m/s^2 (not in g's), and rotational velocity should be in rad/sec
    #
    # If the covariance of the measurement is known, it should be filled in (if all you know is the 
    # variance of each measurement, e.g. from the datasheet, just put those along the diagonal)
    # A covariance matrix of all zeros will be interpreted as "covariance unknown", and to use the
    # data a covariance will have to be assumed or gotten from some other source
    #
    # If you have no estimate for one of the data elements (e.g. your IMU doesn't produce an orientation 
    # estimate), please set element 0 of the associated covariance matrix to -1
    # If you are interpreting this message, please check for a value of -1 in the first element of each 
    # covariance matrix, and disregard the associated estimate.
    
    Header header
    
    geometry_msgs/Quaternion orientation
    float64[9] orientation_covariance # Row major about x, y, z axes
    
    geometry_msgs/Vector3 angular_velocity
    float64[9] angular_velocity_covariance # Row major about x, y, z axes
    
    geometry_msgs/Vector3 linear_acceleration
    float64[9] linear_acceleration_covariance # Row major x, y z 
    
    ================================================================================
    MSG: geometry_msgs/Quaternion
    # This represents an orientation in free space in quaternion form.
    
    float64 x
    float64 y
    float64 z
    float64 w
    
    ================================================================================
    MSG: geometry_msgs/Vector3
    # This represents a vector in free space. 
    # It is only meant to represent a direction. Therefore, it does not
    # make sense to apply a translation to it (e.g., when applying a 
    # generic rigid transformation to a Vector3, tf2 will only apply the
    # rotation). If you want your data to be translatable too, use the
    # geometry_msgs/Point message instead.
    
    float64 x
    float64 y
    float64 z
    ================================================================================
    MSG: sensor_msgs/MagneticField
     # Measurement of the Magnetic Field vector at a specific location.
    
     # If the covariance of the measurement is known, it should be filled in
     # (if all you know is the variance of each measurement, e.g. from the datasheet,
     #just put those along the diagonal)
     # A covariance matrix of all zeros will be interpreted as "covariance unknown",
     # and to use the data a covariance will have to be assumed or gotten from some
     # other source
    
    
     Header header                        # timestamp is the time the
                                          # field was measured
                                          # frame_id is the location and orientation
                                          # of the field measurement
    
     geometry_msgs/Vector3 magnetic_field # x, y, and z components of the
                                          # field vector in Tesla
                                          # If your sensor does not output 3 axes,
                                          # put NaNs in the components not reported.
    
     float64[9] magnetic_field_covariance # Row major about x, y, z axes
                                          # 0 is interpreted as variance unknown
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new imu_msg(null);
    if (msg.Header !== undefined) {
      resolved.Header = std_msgs.msg.Header.Resolve(msg.Header)
    }
    else {
      resolved.Header = new std_msgs.msg.Header()
    }

    if (msg.IMU !== undefined) {
      resolved.IMU = sensor_msgs.msg.Imu.Resolve(msg.IMU)
    }
    else {
      resolved.IMU = new sensor_msgs.msg.Imu()
    }

    if (msg.MagField !== undefined) {
      resolved.MagField = sensor_msgs.msg.MagneticField.Resolve(msg.MagField)
    }
    else {
      resolved.MagField = new sensor_msgs.msg.MagneticField()
    }

    if (msg.IMU_backup !== undefined) {
      resolved.IMU_backup = msg.IMU_backup;
    }
    else {
      resolved.IMU_backup = ''
    }

    return resolved;
    }
};

module.exports = imu_msg;
