# Results

## Reveiver Operating Characteristic Curves (Laparoscopic Dataset)

### Predicting DIED

| Decision Tree      | Random Forest                                        | Neural Network |
| :---        |:-----------------------------------------------------|          :---  |
| ![ROC Curve](./lap_DecisionTreeClassifier_DIED.png)      | ![ROC Curve](./lap_RandomForestClassifier_DIED.png)  | ![ROC Curve](./lap_NeuralNetBinaryClassifier_DIED.png) |

### Predicting LOS

| Decision Tree      | Random Forest                                        | Neural Network                                        |
| :---        |:-----------------------------------------------------|:------------------------------------------------------|
| ![ROC Curve](./lap_DecisionTreeClassifier_LOS.png)      | ![ROC Curve](./lap_RandomForestClassifier_LOS.png)   | ![ROC Curve](./lap_NeuralNetBinaryClassifier_LOS.png) |

### Predicting anastomotic_leak

| Decision Tree      | Random Forest                                                    | Neural Network                                                     |
| :---        |:-----------------------------------------------------------------|:-------------------------------------------------------------------|
| ![ROC Curve](./lap_DecisionTreeClassifier_anastomotic_leak.png)      | ![ROC Curve](./lap_RandomForestClassifier_anastomotic_leak.png)  | ![ROC Curve](./lap_NeuralNetBinaryClassifier_anastomotic_leak.png) |

## Reveiver Operating Characteristic Curves (Open Dataset)

### Predicting DIED

| Decision Tree      | Random Forest                                        | Neural Network                                          |
| :---        |:-----------------------------------------------------|:--------------------------------------------------------|
| ![ROC Curve](./open_DecisionTreeClassifier_DIED.png)      | ![ROC Curve](./open_RandomForestClassifier_DIED.png) | ![ROC Curve](./open_NeuralNetBinaryClassifier_DIED.png) |

### Predicting LOS

| Decision Tree      | Random Forest                                        | Neural Network                                         |
| :---        |:-----------------------------------------------------|:-------------------------------------------------------|
| ![ROC Curve](./open_DecisionTreeClassifier_LOS.png)      | ![ROC Curve](./open_RandomForestClassifier_LOS.png)  | ![ROC Curve](./open_NeuralNetBinaryClassifier_LOS.png) |

### Predicting anastomotic_leak

| Decision Tree      | Random Forest                                                     | Neural Network                                                      |
| :---        |:------------------------------------------------------------------|:--------------------------------------------------------------------|
| ![ROC Curve](./open_DecisionTreeClassifier_anastomotic_leak.png)      | ![ROC Curve](./open_RandomForestClassifier_anastomotic_leak.png)  | ![ROC Curve](./open_NeuralNetBinaryClassifier_anastomotic_leak.png) |
