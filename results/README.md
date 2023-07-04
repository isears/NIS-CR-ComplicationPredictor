# Results

## Reveiver Operating Characteristic Curves (Laparoscopic Dataset)

### Predicting Inpatient Mortality

| Decision Tree      | Random Forest   | Neural Network |
| :---        |    :---   |  :--- |
| ![ROC Curve](./lap_DecisionTreeClassifier_DIED.png)      | ![ROC Curve](./lap_RandomForestClassifier_DIED.png)       | ![ROC Curve](./lap_NeuralNetBinaryClassifier_DIED.png)  |

### Predicting Length of Stay

| Decision Tree      | Random Forest    | Neural Network                                       |
| :---        |    :---    |:-----------------------------------------------------|
| ![ROC Curve](./lap_DecisionTreeClassifier_LOS.png)      | ![ROC Curve](./lap_RandomForestClassifier_LOS.png)       | ![ROC Curve](./lap_NeuralNetBinaryClassifier_LOS.png)  |

### Predicting Anastomotic Leak

| Decision Tree      | Random Forest                                                        | Neural Network                                                     |
| :---        |:---------------------------------------------------------------------|:-------------------------------------------------------------------|
| ![ROC Curve](./lap_DecisionTreeClassifier_anastomotic_leak.png)      | ![ROC Curve](./lap_RandomForestClassifier_anastomotic_leak.png)      | ![ROC Curve](./lap_NeuralNetBinaryClassifier_anastomotic_leak.png) |

## Reveiver Operating Characteristic Curves (Open Dataset)

### Predicting Inpatient Mortality

| Decision Tree      | Random Forest     | Neural Network                                          |
| :---        |    :---  |:--------------------------------------------------------|
| ![ROC Curve](./open_DecisionTreeClassifier_DIED.png)      | ![ROC Curve](./open_RandomForestClassifier_DIED.png)       | ![ROC Curve](./open_NeuralNetBinaryClassifier_DIED.png) |

### Predicting Length of Stay

| Decision Tree      | Random Forest                                            | Neural Network                                  |
| :---        |:---------------------------------------------------------|:------------------------------------------------|
| ![ROC Curve](./open_DecisionTreeClassifier_LOS.png)      | ![ROC Curve](./open_RandomForestClassifier_LOS.png)      | ![ROC Curve](./open_NeuralNetBinaryClassifier_LOS.png) |

### Predicting Anastomotic Leak

| Decision Tree      | Random Forest    | Neural Network                                                      |
| :---        |    :---  |:--------------------------------------------------------------------|
| ![ROC Curve](./open_DecisionTreeClassifier_anastomotic_leak.png)      | ![ROC Curve](./open_RandomForestClassifier_anastomotic_leak.png)       | ![ROC Curve](./open_NeuralNetBinaryClassifier_anastomotic_leak.png)  | ![ROC Curve](./open_NeuralNetBinaryClassifier_anastomotic_leak.png) |
