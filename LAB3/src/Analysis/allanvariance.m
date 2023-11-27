% Load the .bag File
bag = rosbag('C:/Users/steff/OneDrive/Desktop/LAB3RSN/LocationA.bag');

% Select the topic with IMU data
imu_topic = select(bag, 'Topic', '/vectornav');

% Read all messages from the selected topic
msgs = readMessages(imu_topic, 'DataFormat', 'struct');

% Sampling frequency
Fs = 40; 
t0 = 1/Fs;

% Initialize arrays to store the parsed data
angular_velocity = zeros(length(msgs), 3);
accelData = struct('x', [], 'y', [], 'z', []);
gyroData = struct('x', [], 'y', [], 'z', []);
timeStamps = zeros(length(msgs), 1); % Initialize timestamps array

for i = 1:length(msgs)
    val = split(msgs{i}.Data, ',');
    
    % Extract timestamp for each message
    timeStamps(i) = msgs{i}.Header.Stamp.Sec + msgs{i}.Header.Stamp.Nsec * 1e-9;
    
    % Check if the length of the parsed data is as expected
    if length(val) == 13
        % Parse orientation data (yaw, pitch, roll)
        yaw(i) = str2double(val{2});
        pitch(i) = str2double(val{3});
        roll(i) = str2double(val{4});
        
        % Parse magnetometer data
        magX(i) = str2double(val{5});
        magY(i) = str2double(val{6});
        magZ(i) = str2double(val{7});
        
        % Parse accelerometer data
        accelData.x(i) = str2double(val{8});
        accelData.y(i) = str2double(val{9});
        accelData.z(i) = str2double(val{10});
        
        % Parse gyro data
        gyroData.x(i) = str2double(val{11});
        gyroData.y(i) = str2double(val{12});
        calib_gyro_z = split(val{13}, '*');
        gyroData.z(i) = str2double(calib_gyro_z{1});
        
        % Store angular velocity
        angular_velocity(i, :) = [gyroData.x(i), gyroData.y(i), gyroData.z(i)];
    else
        % Handle the case where the data string is not the expected length
        yaw(i) = NaN;
        pitch(i) = NaN;
        roll(i) = NaN;
        magX(i) = NaN;
        magY(i) = NaN;
        magZ(i) = NaN;
        accelData.x(i) = NaN;
        accelData.y(i) = NaN;
        accelData.z(i) = NaN;
        gyroData.x(i) = NaN;
        gyroData.y(i) = NaN;
        gyroData.z(i) = NaN;
        angular_velocity(i, :) = [NaN, NaN, NaN];
    end
end

% Normalize timestamps to start from zero
timeStamps = timeStamps - timeStamps(1);

% Plot time series of Gyroscope data
figure;
plot(timeStamps, gyroData.x, 'r', timeStamps, gyroData.y, 'g', timeStamps, gyroData.z, 'b');
title('Angular Velocity Time Series');
xlabel('Time (s)');
ylabel('Gyro (rad/s)');
legend('x', 'y', 'z');
grid on;

% Plot time series of Accelerometer data
figure;
plot(timeStamps, accelData.x, 'r', timeStamps, accelData.y, 'g', timeStamps, accelData.z, 'b');
title('Linear Acceleration Time Series');
xlabel('Time (s)');
ylabel('Accel (m/s^2)');
legend('x', 'y', 'z');
grid on;

% Calculate noise parameters and plot Allan deviation for Gyroscope
[Nx, Kx, Bx, adevx, taux] = calculateAllanDevAndNoiseParams(gyroData.x, Fs);
[Ny, Ky, By, adevy, tauy] = calculateAllanDevAndNoiseParams(gyroData.y, Fs);
[Nz, Kz, Bz, adevz, tauz] = calculateAllanDevAndNoiseParams(gyroData.z, Fs);

% Allan deviation plot for Gyroscope
figure;
loglog(taux, [adevx, adevy, adevz]);
title('Allan Deviation for Angular Velocity');
xlabel('\tau');
ylabel('\sigma(\tau)');
legend('x', 'y', 'z');
grid on;

% Plot Allan deviation with noise parameters for Gyroscope
plotAllanDevWithNoiseParams(adevx, taux, Nx, Kx, Bx, 'Angular Velocity about X-axis');
plotAllanDevWithNoiseParams(adevy, tauy, Ny, Ky, By, 'Angular Velocity about Y-axis');
plotAllanDevWithNoiseParams(adevz, tauz, Nz, Kz, Bz, 'Angular Velocity about Z-axis');

% Calculate noise parameters and plot Allan deviation for Accelerometer
[Nax, Kax, Bax, adevax, tauax] = calculateAllanDevAndNoiseParams(accelData.x, Fs);
[Nay, Kay, Bay, adevay, tauay] = calculateAllanDevAndNoiseParams(accelData.y, Fs);
[Naz, Kaz, Baz, adevaz, tauaz] = calculateAllanDevAndNoiseParams(accelData.z, Fs);

% Allan deviation plot for Accelerometer
figure;
loglog(tauax, [adevax, adevay, adevaz]);
title('Allan Deviation for Linear Acceleration');
xlabel('\tau');
ylabel('\sigma(\tau)');
legend('x', 'y', 'z');
grid on;

% Plot Allan deviation with noise parameters for Accelerometer
plotAllanDevWithNoiseParams(adevax, tauax, Nax, Kax, Bax, 'Linear Acceleration about X-axis');
plotAllanDevWithNoiseParams(adevay, tauay, Nay, Kay, Bay, 'Linear Acceleration about Y-axis');
plotAllanDevWithNoiseParams(adevaz, tauaz, Naz, Kaz, Baz, 'Linear Acceleration about Z-axis');

% Output noise parameters for Gyroscope
disp('Gyroscope Noise Parameters:');
disp(['N: ' num2str(Nx) ', ' num2str(Ny) ', ' num2str(Nz)]);
disp(['K: ' num2str(Kx) ', ' num2str(Ky) ', ' num2str(Kz)]);
disp(['B: ' num2str(Bx) ', ' num2str(By) ', ' num2str(Bz)]);

% Output noise parameters for Accelerometer
disp('Accelerometer Noise Parameters:');
disp(['N: ' num2str(Nax) ', ' num2str(Nay) ', ' num2str(Naz)]);
disp(['K: ' num2str(Kax) ', ' num2str(Kay) ', ' num2str(Kaz)]);
disp(['B: ' num2str(Bax) ', ' num2str(Bay) ', ' num2str(Baz)]);

% Function to calculate Allan deviation and noise parameters
function [N, K, B, adev, tau] = calculateAllanDevAndNoiseParams(data, Fs)
    t0 = 1/Fs;
    theta = cumsum(data) * t0;
    maxNumM = 100;
    L = length(theta);
    maxM = 2.^floor(log2(L/2));
    m = logspace(log10(1), log10(maxM), maxNumM).';
    m = ceil(m); % m must be an integer.
    m = unique(m); % Remove duplicates.

    tau = m*t0;

    avar = zeros(size(m));
    for i = 1:length(m)
        mi = m(i);
        avar(i) = sum((theta(1+2*mi:end) - 2*theta(1+mi:end-mi) + theta(1:end-2*mi)).^2) / (2*tau(i)^2*(L-2*mi));
    end
    adev = sqrt(avar);
    
    % Angle Random Walk (N)
    slope = -0.5;
    logtau = log10(tau);
    logadev = log10(adev);
    dlogadev = diff(logadev) ./ diff(logtau);
    [~, i] = min(abs(dlogadev - slope));
    b = logadev(i) - slope*logtau(i);
    logN = slope*log10(1) + b;
    N = 10.^logN;

    % Rate Random Walk (K)
    slope = 0.5;
    [~, i] = min(abs(dlogadev - slope));
    b = logadev(i) - slope*logtau(i);
    logK = slope*log10(3) + b;
    K = 10.^logK;

    % Bias Instability (B)
    slope = 0;
    [~, i] = min(abs(dlogadev - slope));
    b = logadev(i) - slope*logtau(i);
    scfB = sqrt(2*log(2)/pi);
    logB = b - log10(scfB);
    B = 10.^logB;

end

% Function to plot Allan deviation with noise parameters
function plotAllanDevWithNoiseParams(adev, tau, N, K, B, axisLabel)
    tauN = 1;
    tauK = 3;
    tauB = tau(find(adev == min(adev), 1));
    params = [N, K, B];
    lineN = N ./ sqrt(tau);
    lineK = K .* sqrt(tau/3);
    scfB = sqrt(2*log(2)/pi);
    lineB = B * scfB * ones(size(tau));
    figure;
    loglog(tau, adev, 'o-', tau, [lineN, lineK, lineB], '--', ...
        [tauN, tauK, tauB], params, 'o');
    
    title(['Allan Deviation of ' axisLabel ' with Noise Parameters']);
    xlabel('\tau');
    ylabel('\sigma(\tau)');
    legend('$\sigma $', '$\sigma_N $','$\sigma_K $', '$\sigma_B $', 'Interpreter', 'latex');
    text([tauN, tauK, tauB], params, {'N', 'K', 'B'});
    grid on;
end
