#include <nuitrack/Nuitrack.h>
#include "NuitrackGLSample.h"
#include <GL/freeglut.h>
#include <GL/glut.h> 
#include <map>
#include <signal.h>
#include <string.h>
#include <iostream>
#include <sstream>
#include <iomanip>
#include <array>
#include <sstream>
#include <arpa/inet.h>
#include <unistd.h>
#include <vector>
#include <cmath>
#include <unordered_map>

NuitrackGLSample sample;

using namespace tdv::nuitrack;
using namespace tdv::nuitrack::device;

#define SERVER_IP "192.168.0.102"  
#define SERVER_PORT 1234

void closeWindow()
{
        sample.release();
        glutDestroyWindow(glutGetWindow());
        exit(EXIT_FAILURE);
}

void display()
{
        // Delegate this action to example's main class
        bool update = sample.update();
        if (!update)
        {
                // End the work if update failed
                closeWindow();
        }

        // Do flush and swap buffers to update viewport
        glFlush();
        glutSwapBuffers();
}

void idle()
{
        glutPostRedisplay();
}

void showHelpInfo()
{
        std::cout << "Usage: nuitrack_gl_sample [path/to/nuitrack.config]\n"
                                 "Press Esc to close window." << std::endl;
}



// Keyboard handler
void keyboard(unsigned char key, int x, int y)
{
        switch (key)
        {
        // On Esc key press
        case 27:
        {
                closeWindow();
        }

        default:
        {
                // Do nothing otherwise
                break;
        }
        }
}

void mouseClick(int button, int state, int x, int y)
{
        if(button == GLUT_LEFT_BUTTON && state == GLUT_DOWN)
        {
                sample.nextViewMode();
        }
}

namespace console {
	namespace interaction {
		int askInt(const std::string& msg, int minValue, int maxValue, bool allowToSkip = false, int defaultValue = -1) {
			const int INVALID_VALUE = minValue - 1;
			int input = INVALID_VALUE;
			do {
				std::cout << msg;
				std::string s;
				std::getline(std::cin, s);

				if (s.empty() && allowToSkip){
					input = defaultValue;
					break;
				}

				if (!s.empty() && !(std::istringstream(s) >> input))
					input = INVALID_VALUE;

			} while (input < minValue || input >= maxValue);

			return input;
		}

		std::string askString(const std::string& msg) {
			std::cout << msg;
			std::string input;
			std::getline(std::cin, input);
			return input;
		}

		bool confirm(const std::string& msg) {
			std::string input;
			do {
				input = askString(msg + " [y/n] ");
			} while (!std::cin.fail() && input != "y" && input != "n");
			return input == "y";
		}
	}

	template<std::size_t Columns>
	class Table {
		using RowType = std::array<std::string, Columns>;

	public:
		Table(RowType&& header): _header(header) {
			for (std::size_t i = 0; i < Columns; ++i)
				_maxColumnLengths[i] = _header[i].length();
		}

		void addRow(RowType&& row) {
			_updateColumnLengths(row);
			_rows.push_back(std::move(row));
		}

		void printTable() const  {
			_printHeader(_header);
			for (const auto& row: _rows)
				_printRow(row);
		}

	private:
		void _updateColumnLengths(const RowType& row) {
			for (std::size_t i = 0; i < Columns; ++i) {
				const auto length = row[i].length();
				if (length > _maxColumnLengths[i])
					_maxColumnLengths[i] = length;
			}
		}

		void _printHeader(const RowType& header) const {
			for (std::size_t i = 0; i < Columns - 1; ++i)
				std::cout << ' ' << _centered(header[i], _maxColumnLengths[i]) << " |";
			std::cout << ' ' << _centered(header[Columns - 1], _maxColumnLengths[Columns - 1]) << '\n';
		}

		void _printRow(const RowType& row) const {
			for (std::size_t i = 0; i < Columns - 1; ++i)
				std::cout << ' ' << std::setw(_maxColumnLengths[i]) << row[i] << " |";
			std::cout << ' ' << std::setw(_maxColumnLengths[Columns - 1]) << row[Columns - 1] << '\n';
		}

		static std::string _centered(const std::string& original, int targetSize) {
			const auto padding = targetSize - original.size();
			if (padding > 0) {
				const auto paddingRight = padding / 2;
				const auto paddingLeft = padding - paddingRight;
				return std::string(paddingLeft, ' ') + original + std::string(paddingRight, ' ');
			}
			return original;
		}

	private:
		const RowType _header;
		std::vector<RowType> _rows;
		std::array<std::size_t, Columns> _maxColumnLengths;
	};

} // namespace console

std::string toString(ActivationStatus status) {
	switch (status) {
		case ActivationStatus::NONE: return "None";
		case ActivationStatus::TRIAL: return "Trial";
		case ActivationStatus::PRO: return "Pro";
		default: return "Unknown type";
	}
}

NuitrackDevice::Ptr selectDevice() {
		std::vector<NuitrackDevice::Ptr> devices;
		while (true)
		{
			devices = Nuitrack::getDeviceList();
			
			if (!devices.empty())
				break;

			std::cout << "\nConnect sensor and press Enter to continue" << std::endl;
			std::cin.ignore();
		}


		int devIndex = 0;

		return devices[devIndex];
}

void selectDeviceVideoMode(NuitrackDevice::Ptr device, StreamType streamType) {
	std::string streamName;
	switch (streamType) {
		case StreamType::DEPTH:
			streamName = "depth"; break;
		case StreamType::COLOR:
			streamName = "color"; break;
	}

	const auto videoModes = device->getAvailableVideoModes(streamType);
	const auto vmSize = videoModes.size();


	int vmIndex = 0;
	device->setVideoMode(streamType, videoModes[vmIndex]);
}

void activateDevice(NuitrackDevice::Ptr device) {
		bool isActivated = true;

		if (isActivated)
			isActivated = true;

		if (!isActivated) {
			std::string activationKey = console::interaction::askString("Enter the activation key: ");
			device->activate(activationKey);
			std::cout << "Activation status: " << toString(device->getActivationStatus()) << std::endl;
		}
}

void onNewDepthFrameCallback(DepthFrame::Ptr frame) {
	if (frame)
		std::cout << "Nuitrack received Depth Frame [" << frame->getTimestamp() << "]: " << frame->getCols() <<  " x " << frame->getRows() << '\n';
}

void onNewColorFrameCallback(RGBFrame::Ptr frame) {
	if (frame)
		std::cout << "Nuitrack received Color Frame [" << frame->getTimestamp() << "]: " << frame->getCols() <<  " x " << frame->getRows() << '\n';
}

void sendDataToPython(const std::string& data)
{
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        std::cerr << "Socket creation failed!\n";
        return;
    }

    struct sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(SERVER_PORT);
    inet_pton(AF_INET, SERVER_IP, &serverAddr.sin_addr);

    if (connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        std::cerr << "Connection to Python server failed!\n";
        close(sock);
        return;
    }

    send(sock, data.c_str(), data.length(), 0);
    close(sock);
}


double computeAngle(const tdv::nuitrack::Vector3& vecA, const tdv::nuitrack::Vector3& vecB)
{
    double dotProduct = vecA.x * vecB.x + vecA.y * vecB.y + vecA.z * vecB.z;
    double magnitudeA = sqrt(vecA.x * vecA.x + vecA.y * vecA.y + vecA.z * vecA.z);
    double magnitudeB = sqrt(vecB.x * vecB.x + vecB.y * vecB.y + vecB.z * vecB.z);
    
    if (magnitudeA == 0 || magnitudeB == 0) return 0.0; // Avoid division by zero

    double cosineTheta = dotProduct / (magnitudeA * magnitudeB);
    return acos(cosineTheta) * (180.0 / M_PI);  // Convert radians to degrees
}

std::unordered_map<int, std::unordered_map<tdv::nuitrack::JointType, std::pair<double, double>>> previousAngles;

double computeAngle2D(double x1, double y1, double x2, double y2)
{
    double dotProduct = x1 * x2 + y1 * y2;
    double magnitudeA = sqrt(x1 * x1 + y1 * y1);
    double magnitudeB = sqrt(x2 * x2 + y2 * y2);

    if (magnitudeA == 0 || magnitudeB == 0) return 0.0; // Avoid division by zero

    double cosineTheta = dotProduct / (magnitudeA * magnitudeB);
    return acos(cosineTheta) * (180.0 / M_PI);  // Convert radians to degrees
}

void onNewSkeletonCallback(SkeletonData::Ptr skeletonData)
{
    if (!skeletonData) {
        std::cout << "No skeleton data received.\n";
        return;
    }

    int numSkeletons = skeletonData->getNumSkeletons();
    std::cout << "Nuitrack detected " << numSkeletons << " skeletons\n";

    if (numSkeletons == 0) return;

    for (const auto& skeleton : skeletonData->getSkeletons())
    {
        std::stringstream dataStream;
		if(skeleton.id == 1){

        struct JointPair {
            tdv::nuitrack::JointType parent, child, grandchild;
            std::string name;
            bool isBallJoint;
        };

        std::vector<JointPair> jointPairs = {
            // Shoulders
            {tdv::nuitrack::JointType::JOINT_NECK, tdv::nuitrack::JointType::JOINT_LEFT_SHOULDER, tdv::nuitrack::JointType::JOINT_LEFT_ELBOW, "Left Shoulder", true},
            {tdv::nuitrack::JointType::JOINT_NECK, tdv::nuitrack::JointType::JOINT_RIGHT_SHOULDER, tdv::nuitrack::JointType::JOINT_RIGHT_ELBOW, "Right Shoulder", true},
            // Elbows
            {tdv::nuitrack::JointType::JOINT_LEFT_SHOULDER, tdv::nuitrack::JointType::JOINT_LEFT_ELBOW, tdv::nuitrack::JointType::JOINT_LEFT_HAND, "Left Elbow", false},
            {tdv::nuitrack::JointType::JOINT_RIGHT_SHOULDER, tdv::nuitrack::JointType::JOINT_RIGHT_ELBOW, tdv::nuitrack::JointType::JOINT_RIGHT_HAND, "Right Elbow", false},
            // Hips
            {tdv::nuitrack::JointType::JOINT_TORSO, tdv::nuitrack::JointType::JOINT_LEFT_HIP, tdv::nuitrack::JointType::JOINT_LEFT_KNEE, "Left Hip", true},
            {tdv::nuitrack::JointType::JOINT_TORSO, tdv::nuitrack::JointType::JOINT_RIGHT_HIP, tdv::nuitrack::JointType::JOINT_RIGHT_KNEE, "Right Hip", true},
            // Knees
            {tdv::nuitrack::JointType::JOINT_LEFT_HIP, tdv::nuitrack::JointType::JOINT_LEFT_KNEE, tdv::nuitrack::JointType::JOINT_LEFT_FOOT, "Left Knee", false},
            {tdv::nuitrack::JointType::JOINT_RIGHT_HIP, tdv::nuitrack::JointType::JOINT_RIGHT_KNEE, tdv::nuitrack::JointType::JOINT_RIGHT_FOOT, "Right Knee", false}
        };

        for (const auto& jointSet : jointPairs)
        {
            Joint parent = skeleton.joints[jointSet.parent];
            Joint child = skeleton.joints[jointSet.child];
            Joint grandchild = skeleton.joints[jointSet.grandchild];

            double angleXY = 0.0, angleYZ = 0.0;

            if (parent.confidence < 0.5 || child.confidence < 0.5 || grandchild.confidence < 0.5)
            {
                // Use previously stored angles if available
                if (previousAngles[skeleton.id].count(jointSet.child))
                {
                    auto prevAngles = previousAngles[skeleton.id][jointSet.child];
                    angleXY = prevAngles.first;
                    angleYZ = prevAngles.second;
                }
            }
            else
            {
                // Calculate new angles
                tdv::nuitrack::Vector3 vecA = {child.real.x - parent.real.x, child.real.y - parent.real.y, child.real.z - parent.real.z};
                tdv::nuitrack::Vector3 vecB = {grandchild.real.x - child.real.x, grandchild.real.y - child.real.y, grandchild.real.z - child.real.z};

                if (jointSet.isBallJoint)  // Shoulders and Hips
                {
                    angleXY = computeAngle2D(vecA.x, vecA.y, vecB.x, vecB.y);
                    angleYZ = computeAngle2D(vecA.y, vecA.z, vecB.y, vecB.z);
                }
                else  // Elbows and Knees (hinge joints)
                {
                    angleXY = computeAngle(vecA, vecB);
                    angleYZ = 0.0;  // Not needed for hinge joints
                }

                // Store new angles
                previousAngles[skeleton.id][jointSet.child] = {angleXY, angleYZ};
            }

            // Append to output stream
			if(jointSet.isBallJoint){
            dataStream << angleXY << " " << angleYZ << " ";
			}else{
				dataStream <<angleXY<<" ";
			}
        }

        std::string skeletonDataStr = dataStream.str();
        std::cout << skeletonDataStr;  // Print angles

        sendDataToPython(skeletonDataStr);  // Send to Python server

        std::cout << "-----------------------\n";
		}
    }
}




bool finished;
void signalHandler(int signal) {
	if (signal == SIGINT)
		finished = true;
}

int main(int argc, char* argv[]) {
	int errorCode = EXIT_SUCCESS;

	try {
		Nuitrack::init();

		const auto device = selectDevice();

		activateDevice(device);

		if (true) {
			selectDeviceVideoMode(device, StreamType::DEPTH);
			selectDeviceVideoMode(device, StreamType::COLOR);

			Nuitrack::setDevice(device);

			auto depthSensor = DepthSensor::create();
			auto colorSensor = ColorSensor::create();
			auto skeletonTracker = SkeletonTracker::create();

			depthSensor->connectOnNewFrame(onNewDepthFrameCallback);
			colorSensor->connectOnNewFrame(onNewColorFrameCallback);
			skeletonTracker->connectOnUpdate(onNewSkeletonCallback);

			Nuitrack::run();

			signal(SIGINT, &signalHandler);
			while (!finished){

				        // Prepare sample to work
        if (argc < 2)
                sample.init();
        else
                sample.init(argv[1]);

        auto outputMode = sample.getOutputMode();

        // Initialize GLUT window
        glutInit(&argc, argv);
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH);
        glutInitWindowSize(outputMode.xres, outputMode.yres);
        glutCreateWindow("Nuitrack GL Sample (Nuitrack API)");
        //glutSetCursor(GLUT_CURSOR_NONE);

        // Connect GLUT callbacks
        glutKeyboardFunc(keyboard);
        glutDisplayFunc(display);
        glutIdleFunc(idle);
        glutMouseFunc(mouseClick);
        glutCloseFunc(closeWindow);

        // Setup OpenGL
        glDisable(GL_DEPTH_TEST);
        glEnable(GL_TEXTURE_2D);

        glEnableClientState(GL_VERTEX_ARRAY);
        glDisableClientState(GL_COLOR_ARRAY);


        glOrtho(0, outputMode.xres, outputMode.yres, 0, -1.0, 1.0);
        glMatrixMode(GL_PROJECTION);
        glPushMatrix();
        glLoadIdentity();

        // Start main loop
        glutMainLoop();
				Nuitrack::waitUpdate(skeletonTracker);
			}
		}
	}
	catch (const LicenseNotAcquiredException& e)
	{
		std::cerr << "LicenseNotAcquired exception (ExceptionType: " << e.type() << ')' << std::endl;
		errorCode = EXIT_FAILURE;
	}
	catch (const Exception& e)
	{
		std::cerr << "Exception: " << e.what() << std::endl;
		errorCode = EXIT_FAILURE;
	}
        showHelpInfo();



	Nuitrack::release();
	return errorCode;
}