# T2D Prediction System: Data Fusion for Enhanced Decision Making

## Project Overview

The T2D Prediction System is a comprehensive healthcare solution designed to predict and manage Type 2 Diabetes (T2D) risk through advanced data fusion techniques. This innovative platform combines clinical and genetic data to provide healthcare professionals with accurate risk assessments and management tools for better patient outcomes. By leveraging artificial intelligence and machine learning algorithms, our system offers a holistic approach to diabetes risk prediction that surpasses traditional single-source prediction methods.

Developed with a focus on precision medicine, this system integrates diverse datasets from multiple populations including African American, Bangladeshi, and Iraqi cohorts to ensure robust predictions across different demographic groups. The data fusion approach employed in this project enhances prediction accuracy by considering both clinical markers and genetic factors that contribute to T2D risk, providing a more complete picture than either data source could offer independently.

The platform features a user-friendly web interface that allows healthcare providers to input patient data, receive instant risk predictions with confidence scoring, track patient metrics over time, and access an AI assistant for personalized treatment recommendations. This comprehensive solution aims to transform diabetes management by enabling data-driven decision making and early intervention strategies.

## System Architecture

The T2D Prediction System employs a modern, scalable architecture consisting of three main components: data processing pipelines, machine learning models, and a full-stack web application.

The data processing component includes several Jupyter notebooks (African_American.ipynb, Bangladesh.ipynb, Iraq.ipynb, genetic.ipynb, and Data_Fusion.ipynb) that handle the preprocessing, cleaning, and integration of diverse datasets. These notebooks document the methodologies used to prepare both clinical and genetic data for model training and fusion.

At the core of the system are sophisticated machine learning models implemented using TensorFlow/Keras, which are saved as fusion_model_final0.keras and fusion_model_percentage.h5. These models are the result of extensive experimentation and validation to ensure optimal performance in predicting T2D risk by fusing multiple data sources.

The web application follows a client-server architecture with a clear separation between frontend and backend components:

The backend is built with Python using FastAPI, providing RESTful API endpoints for authentication, prediction, and data management. It includes database integration (using SQLite for development), user authentication, and model serving capabilities. The backend handles all computational tasks including running the prediction models and storing user data securely.

The frontend is developed using React.js with Tailwind CSS for styling, offering a responsive and intuitive user interface. It includes multiple pages for different functionalities such as home, dashboard, prediction, and AI assistant features. The frontend communicates with the backend through API calls to retrieve predictions and manage user data.

This architecture ensures scalability, maintainability, and a smooth user experience while handling complex data processing and prediction tasks behind the scenes.

## Installation and Setup

### Prerequisites

Before installing the T2D Prediction System, ensure you have the following prerequisites installed on your system:

- Python 3.8 or higher
- Node.js 14.x or higher
- npm 6.x or higher
- Git

### Backend Setup

To set up the backend of the T2D Prediction System, follow these detailed steps:

1. Clone the repository to your local machine using Git:
   ```
   git clone https://github.com/yourusername/T2D-Prediction-System--Data-Fusion-for-Enhanced-Decision-Making.git
   cd T2D-Prediction-System--Data-Fusion-for-Enhanced-Decision-Making
   ```

2. Create and activate a Python virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required Python dependencies:
   ```
   cd backend
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   cd backend
   python create_db.py
   ```

5. Start the backend server:
   ```
   python main.py
   ```

The backend server will start running on http://localhost:8000 by default, providing API endpoints for the frontend application.

### Frontend Setup

To set up the frontend of the T2D Prediction System, follow these steps:

1. Navigate to the frontend directory:
   ```
   cd frontend/app/diabetes-tracker
   ```

2. Install the required Node.js dependencies:
   ```
   npm install
   ```

3. Configure the environment variables by creating a .env file in the frontend directory with the following content:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```
   npm start
   ```

The frontend application will start running on http://localhost:3000, providing access to the user interface of the T2D Prediction System.

### Production Deployment

For production deployment, additional steps are recommended:

1. Build the frontend for production:
   ```
   cd frontend/app/diabetes-tracker
   npm run build
   ```

2. Deploy the backend using a production-ready server such as Gunicorn:
   ```
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
   ```

3. Use a reverse proxy like Nginx to serve the frontend build files and route API requests to the backend server.

4. Consider using environment variables for sensitive configuration settings in production.

## Usage Guide

The T2D Prediction System offers a comprehensive suite of features designed to assist healthcare professionals in predicting and managing Type 2 Diabetes risk. This section provides detailed guidance on how to effectively use the system.

### User Registration and Authentication

Upon accessing the system, new users must register by providing their professional credentials. This ensures that the system is used by qualified healthcare providers. After registration, users can log in to access the full functionality of the platform. The authentication system ensures that patient data remains secure and is only accessible to authorized personnel.

### Dashboard Overview

After logging in, users are presented with a comprehensive dashboard that provides an overview of their patients' data and risk assessments. The dashboard displays key metrics such as the number of patients monitored, average risk scores, and recent predictions. This gives healthcare providers a quick snapshot of their patient population's diabetes risk status.

### Performing T2D Risk Prediction

To perform a new risk prediction, navigate to the "Start Tracking" section from the main menu. Here, you can input both clinical and genetic data for a patient:

Clinical data includes parameters such as age, gender, BMI, blood glucose levels, family history, and other relevant health metrics. The system is designed to work with standard clinical measurements that are routinely collected during patient examinations.

Genetic data can be input based on specific genetic markers known to be associated with T2D risk. The system supports various genetic data formats and provides guidance on which genetic markers are most relevant for prediction.

Once all required data is entered, click the "Predict" button to generate a risk assessment. The system processes the input data through its fusion model and returns a comprehensive prediction result.

### Interpreting Prediction Results

The prediction results page displays the calculated risk of T2D development along with a confidence score. The risk is presented as a percentage, indicating the likelihood of the patient developing T2D based on their clinical and genetic profile. The confidence score reflects the reliability of the prediction based on the quality and completeness of the input data.

Additionally, the system provides a breakdown of contributing factors, highlighting which clinical or genetic markers are most significantly influencing the risk prediction. This information is valuable for developing targeted intervention strategies.

### Using the AI Assistant

The T2D Prediction System includes an integrated AI assistant that can provide guidance on interpreting results and suggesting potential treatment or prevention plans. To use this feature, navigate to the "Assistant" section from the main menu or click on the "Ask Assistant" button on the prediction results page.

You can copy prediction results directly to the assistant and ask specific questions about management strategies, lifestyle modifications, or medication options based on the patient's risk profile. The assistant uses advanced natural language processing to provide evidence-based recommendations tailored to the specific patient case.

### Tracking Patient Progress

The system allows for longitudinal tracking of patient data and risk assessments. Each prediction can be saved to the patient's profile, enabling healthcare providers to monitor changes in risk over time. This feature is particularly valuable for assessing the effectiveness of interventions and treatment plans.

To access historical data, navigate to the patient's profile page where all previous predictions and measurements are displayed in chronological order. The system also generates trend visualizations to help identify patterns and changes in risk factors over time.

## Features Description

The T2D Prediction System offers a comprehensive set of features designed to revolutionize diabetes risk assessment and management. These features have been carefully developed to meet the needs of healthcare professionals while ensuring ease of use and clinical relevance.

### Data Fusion Prediction Model

At the heart of our system lies the innovative data fusion prediction model that combines clinical and genetic information to generate highly accurate T2D risk assessments. Unlike traditional prediction methods that rely on a single data source, our fusion approach integrates multiple data types to provide a more comprehensive understanding of diabetes risk factors. This model has been trained on diverse population datasets including African American, Bangladeshi, and Iraqi cohorts, ensuring robust performance across different demographic groups.

The fusion model employs advanced machine learning techniques to identify complex patterns and relationships between clinical markers and genetic factors that contribute to T2D risk. By considering both environmental and genetic influences, the system can detect subtle risk indicators that might be missed by conventional assessment methods. This holistic approach significantly improves prediction accuracy and enables more personalized risk stratification.

### Real-Time Prediction with Confidence Scoring

The system provides instantaneous risk predictions upon data submission, eliminating the waiting period typically associated with comprehensive health assessments. Each prediction is accompanied by a confidence score that indicates the reliability of the assessment based on the quality and completeness of the input data. This transparency helps healthcare providers make informed decisions about the weight they should give to the prediction in their clinical judgment.

The real-time nature of the prediction system allows for immediate discussion with patients about their risk factors and potential intervention strategies. This timely feedback can be a powerful motivator for patient engagement in preventive measures and lifestyle modifications.

### Comprehensive Dashboard for Patient Monitoring

The interactive dashboard offers healthcare providers a centralized platform for monitoring patient metrics and risk status. The system automatically logs key health indicators such as glucose levels, BMI, and risk scores, presenting them in an intuitive interface that highlights trends and changes over time. This longitudinal view of patient data enables providers to track the effectiveness of interventions and adjust treatment plans accordingly.

The dashboard also includes population-level analytics that allow providers to identify patterns across their patient cohorts. These insights can inform practice-wide initiatives and resource allocation for diabetes prevention and management programs.

### AI-Powered Assistant for Clinical Decision Support

The integrated AI assistant serves as a virtual consultant, offering evidence-based suggestions for treatment and prevention strategies based on individual patient risk profiles. This feature leverages natural language processing to understand complex clinical queries and provide relevant, actionable recommendations drawn from medical literature and clinical guidelines.

Healthcare providers can interact with the assistant using conversational language, asking specific questions about patient management or requesting clarification on risk factors. The assistant can explain prediction results in plain language, suggest targeted interventions for specific risk factors, and provide references to relevant clinical studies or guidelines. This support tool enhances clinical decision-making while keeping the healthcare provider firmly in control of patient care.

### Secure Multi-User Environment

The system implements robust authentication and authorization protocols to ensure that patient data remains secure and is only accessible to authorized healthcare professionals. Each user has a personalized account with appropriate access permissions based on their role and responsibilities. This multi-user environment facilitates collaboration among healthcare team members while maintaining strict data privacy standards.

The platform complies with healthcare data security best practices, including encrypted data storage and transmission, secure authentication mechanisms, and comprehensive audit logging of all system activities. These security measures protect sensitive patient information while enabling the collaborative care approach that is essential for effective diabetes management.

## Data and Models Explanation

The T2D Prediction System leverages a sophisticated approach to data processing and modeling that forms the foundation of its predictive capabilities. This section provides an in-depth explanation of the datasets, preprocessing methodologies, and machine learning models employed in the system.

### Datasets

The system utilizes diverse datasets from multiple populations to ensure robust and generalizable predictions across different demographic groups. These datasets include:

Clinical Data: Comprehensive clinical records from African American, Bangladeshi, and Iraqi populations, containing parameters such as age, gender, BMI, blood glucose levels, blood pressure, family history of diabetes, and other relevant health metrics. These datasets are stored in the processed_datasets/clinical directory and include African_pro.csv, Bangladesh_pro.csv, Iraq_pro.csv, and a merged file merged_clinical_full.csv that combines data from all populations.

Genetic Data: Genetic markers known to be associated with T2D risk, collected from various populations. These datasets include single nucleotide polymorphisms (SNPs) and other genetic variants that have been identified through genome-wide association studies (GWAS) as having significant correlations with T2D development. The genetic datasets are stored in the processed_datasets/genetic directory and include normal_genetic_dataset.csv, inter_genetic_dataset.csv, and merged_genetic_full.csv.

The diversity of these datasets enables the system to account for population-specific risk factors and genetic variations, resulting in more personalized and accurate predictions for patients from different ethnic backgrounds.

### Data Preprocessing and Feature Engineering

The data preprocessing pipeline is documented in several Jupyter notebooks (African_American.ipynb, Bangladesh.ipynb, Iraq.ipynb, genetic.ipynb) that detail the steps taken to clean, normalize, and prepare the data for model training. These preprocessing steps include:

Handling missing values through appropriate imputation techniques based on the nature of each variable.
Normalizing numerical features to ensure consistent scaling across different measurements.
Encoding categorical variables using methods such as one-hot encoding or label encoding.
Feature selection to identify the most predictive variables from both clinical and genetic datasets.
Feature engineering to create derived variables that capture complex relationships between raw data points.

The Data_Fusion.ipynb notebook specifically documents the methodology used to integrate clinical and genetic data, addressing challenges such as different scales, dimensionality, and information content between these disparate data sources.

### Machine Learning Models

The core predictive capability of the system is powered by advanced machine learning models that have been carefully designed and optimized for T2D risk prediction:

Fusion Model Architecture: The system employs a neural network-based fusion model that processes clinical and genetic data through separate pathways before combining them in deeper layers of the network. This architecture allows the model to learn both data type-specific patterns and cross-modal relationships that contribute to T2D risk.

Model Training and Validation: The models were trained using a rigorous cross-validation approach to ensure generalizability across different patient populations. The training process included hyperparameter optimization to find the optimal model configuration for maximum prediction accuracy.

Model Evaluation: The performance of the fusion model was evaluated using metrics such as accuracy, precision, recall, F1-score, and area under the ROC curve (AUC). The evaluation results, documented in evaluation_report.txt, demonstrate the superior performance of the fusion approach compared to models trained on either clinical or genetic data alone.

The trained models are saved in two formats:
- fusion_model_final0.keras: The primary model used for production predictions.
- fusion_model_percentage.h5: An alternative model that provides risk predictions as percentage values.

These models are loaded by the backend server during runtime to generate predictions based on user-provided data. The model serving infrastructure is designed to handle concurrent prediction requests efficiently while maintaining consistent performance.

### Continuous Improvement

The T2D Prediction System is designed with a framework for continuous model improvement as new data becomes available. The modular architecture allows for:

Retraining models with additional data to improve prediction accuracy over time.
Incorporating new genetic markers as research identifies additional T2D-associated variants.
Updating the fusion methodology to leverage advances in machine learning techniques.

This commitment to ongoing refinement ensures that the system remains at the cutting edge of T2D risk prediction technology, providing healthcare professionals with increasingly accurate and personalized risk assessments.

## License Information

The T2D Prediction System is licensed under the [Apache License 2.0](LICENSE), a permissive open-source license that allows broad usage, modification, and distribution while providing protections for contributors, including patent rights.

You are free to use, modify, and distribute this software under the conditions of the license. However, you must preserve the original copyright notice and include a NOTICE file with any significant modifications.

> Copyright [2024] Abdullah Dahabre and contributors  
> Licensed under the Apache License, Version 2.0 (the "License");  
> you may not use this file except in compliance with the License.  
> You may obtain a copy of the License at  
> https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software  
distributed under the License is distributed on an "AS IS" BASIS,  
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
See the License for the specific language governing permissions and  
limitations under the License.

## Acknowledgments

The development of the T2D Prediction System was made possible through the contributions of numerous individuals and organizations. We extend our sincere gratitude to all those who provided data, expertise, and support throughout the project.

Special thanks to the research teams who collected and shared the clinical and genetic datasets from African American, Bangladeshi, and Iraqi populations, which were instrumental in training and validating our prediction models. Their commitment to advancing diabetes research has been invaluable to this project.

We also acknowledge the open-source community whose tools and libraries form the foundation of our system. This includes the developers of TensorFlow, Keras, React, FastAPI, and numerous other technologies that enabled the creation of this comprehensive platform.

Finally, we thank the healthcare professionals who provided feedback during the development process, helping to ensure that the system meets the practical needs of those working directly with patients at risk of Type 2 Diabetes.

## Contact and Support

For questions, feedback, or support regarding the T2D Prediction System, please contact the development team at abdzahirmoh@gmail.com. We welcome contributions from the community and are committed to continuously improving the system based on user feedback and advances in diabetes research.

For technical issues or feature requests, please submit an issue through the project's GitHub repository. For collaboration inquiries or partnership opportunities, please contact our team directly at abdzahirmoh@gmail.com.

Our documentation is regularly updated to reflect new features and improvements. Visit our website at https://webapp-frontend-voa8.vercel.app/ for the latest information and resources related to the T2D Prediction System.
