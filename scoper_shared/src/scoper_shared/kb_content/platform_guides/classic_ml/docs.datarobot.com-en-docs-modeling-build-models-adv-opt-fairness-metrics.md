[ DataRobot docs ](../../../index.html "DataRobot docs")

  * [ Data ](../../../data/index.html) [ Data ](../../../data/index.html)
    * [ Data connections ](../../../data/connect-data/index.html) [ Data connections ](../../../data/connect-data/index.html)
      * [ Share secure configurations ](../../../data/connect-data/secure-config.html)
      * [ Data connections ](../../../data/connect-data/data-conn.html)
    * [ AI Catalog ](../../../data/ai-catalog/index.html) [ AI Catalog ](../../../data/ai-catalog/index.html)
      * [ Load data ](../../../data/ai-catalog/catalog.html)
      * [ Manage assets ](../../../data/ai-catalog/manage-asset.html)
      * [ Work with assets ](../../../data/ai-catalog/catalog-asset.html)
      * [ Schedule snapshots ](../../../data/ai-catalog/snapshot.html)
      * [ Prepare data with Spark SQL ](../../../data/ai-catalog/spark.html)
    * [ Import data ](../../../data/import-data/index.html) [ Import data ](../../../data/import-data/index.html)
      * [ Import to DataRobot directly ](../../../data/import-data/import-to-dr.html)
      * [ Large datasets ](../../../data/import-data/large-data/index.html) [ Large datasets ](../../../data/import-data/large-data/index.html)
        * [ Fast EDA for large datasets ](../../../data/import-data/large-data/fast-eda.html)
    * [ Transform data ](../../../data/transform-data/index.html) [ Transform data ](../../../data/transform-data/index.html)
      * [ Interaction-based transformations ](../../../data/transform-data/feature-disc.html)
      * [ Feature Discovery ](../../../data/transform-data/feature-discovery/index.html) [ Feature Discovery ](../../../data/transform-data/feature-discovery/index.html)
        * [ End-to-end Feature Discovery ](../../../data/transform-data/feature-discovery/enrich-data-using-feature-discovery.html)
        * [ Set up Feature Discovery projects ](../../../data/transform-data/feature-discovery/fd-overview.html)
        * [ Snowflake integration ](../../../data/transform-data/feature-discovery/fd-snowflake.html)
        * [ Feature Discovery settings ](../../../data/transform-data/feature-discovery/fd-adv-opt.html)
        * [ Time-aware feature engineering ](../../../data/transform-data/feature-discovery/fd-time.html)
        * [ Derived features ](../../../data/transform-data/feature-discovery/fd-gen.html)
        * [ Predictions ](../../../data/transform-data/feature-discovery/fd-predict.html)
      * [ Manual transformations ](../../../data/transform-data/feature-transforms.html)
    * [ Analyze data ](../../../data/analyze-data/index.html) [ Analyze data ](../../../data/analyze-data/index.html)
      * [ Assess data quality with EDA ](../../../data/analyze-data/assess-data-quality-eda.html)
      * [ Analyze features using histograms ](../../../data/analyze-data/analyze-histogram.html)
      * [ Analyze frequent values ](../../../data/analyze-data/analyze-frequent-values.html)
      * [ Feature details ](../../../data/analyze-data/histogram.html)
      * [ Exploratory Spatial Data Analysis (ESDA) ](../../../data/analyze-data/lai-esda.html)
      * [ Feature Associations ](../../../data/analyze-data/feature-assoc.html)
      * [ Use data pipelines for ingest and transformation ](../../../data/analyze-data/pipelines.html)
    * [ Data preview features ](../../../data/data-preview/index.html) [ Data preview features ](../../../data/data-preview/index.html)
      * [ Create feature lists in the Relationship Editor ](../../../data/data-preview/safer-rel-editor-feature-lists.html)
    * [ Data FAQ ](../../../data/data-faq.html)
  * [ Modeling ](../../index.html) [ Modeling ](../../index.html)
    * [ Build models ](../index.html) [ Build models ](../index.html)
      * [ Build models ](../build-basic/index.html) [ Build models ](../build-basic/index.html)
        * [ Basic model workflow ](../build-basic/model-data.html)
        * [ Work with feature lists ](../build-basic/feature-lists.html)
        * [ Unlock Holdout ](../build-basic/unlocking-holdout.html)
        * [ Comprehensive Autopilot ](../build-basic/more-accuracy.html)
        * [ Add/delete models ](../build-basic/creating-addl-models.html)
        * [ Frozen runs ](../build-basic/frozen-run.html)
        * [ Model Repository ](../build-basic/repository.html)
      * [ Advanced options ](index.html) [ Advanced options ](index.html)
        * [ Additional ](additional.html)
        * [ Bias and Fairness ](fairness-metrics.html) [ Bias and Fairness ](fairness-metrics.html)

[For Self-Managed AI Platform users running v11.1, see the on-premise platform
documentation __](/11.1/en/docs/index.html)

Bias and Fairness

          * Configure metrics and mitigation pre-Autopilot 
            * Set fairness metrics 
            * Set mitigation techniques 
          * Configure metrics and mitigation post-Autopilot 
            * Retrain with fairness tests 
            * Retrain with mitigation 
              * Single-model retraining 
              * Multiple-model retraining 
            * Identify mitigated models 
            * Compare models 
          * Mitigation eligibility 
          * Bias mitigation considerations 

        * [ Clustering advanced options ](time-series-cluster-adv-opt.html)
        * [ External Predictions ](external-preds.html)
        * [ Feature Constraints ](feature-con.html)
        * [ Image Augmentation ](ttia.html)
        * [ Partitioning ](partitioning.html)
        * [ Smart Downsampling ](smart-ds.html)
        * [ Time series ](time-series-adv-opt.html)
        * [ GPUs for deep learning ](gpus.html)
    * [ Model insights ](../../analyze-models/index.html) [ Model insights ](../../analyze-models/index.html)
      * [ Evaluate ](../../analyze-models/evaluate/index.html) [ Evaluate ](../../analyze-models/evaluate/index.html)
        * [ Accuracy Over Space ](../../special-workflows/location-ai/lai-insights.html)
        * [ Accuracy Over Time ](../../analyze-models/evaluate/aot.html)
        * [ Advanced Tuning ](../../analyze-models/evaluate/adv-tuning.html)
        * [ Anomaly visualizations ](../../analyze-models/evaluate/anom-viz.html)
        * [ Confusion Matrix (for multiclass models) ](../../analyze-models/evaluate/multiclass.html)
        * [ Forecasting Accuracy ](../../analyze-models/evaluate/forecast-acc.html)
        * [ Forecast vs Actual ](../../analyze-models/evaluate/fore-act.html)
        * [ Lift Chart ](../../analyze-models/evaluate/lift-chart.html)
        * [ Period Accuracy ](../../analyze-models/evaluate/period-accuracy.html)
        * [ Residuals ](../../analyze-models/evaluate/residuals.html)
        * [ ROC Curve tools ](../../analyze-models/evaluate/roc-curve-tab/index.html) [ ROC Curve tools ](../../analyze-models/evaluate/roc-curve-tab/index.html)
          * [ Use the ROC Curve tools ](../../analyze-models/evaluate/roc-curve-tab/roc-curve-tab-use.html)
          * [ Select data and display threshold ](../../analyze-models/evaluate/roc-curve-tab/threshold.html)
          * [ Confusion matrix ](../../analyze-models/evaluate/roc-curve-tab/confusion-matrix.html)
          * [ Prediction Distribution graph ](../../analyze-models/evaluate/roc-curve-tab/pred-dist-graph.html)
          * [ ROC curve ](../../analyze-models/evaluate/roc-curve-tab/roc-curve.html)
          * [ Profit curve ](../../analyze-models/evaluate/roc-curve-tab/profit-curve.html)
          * [ Cumulative Charts ](../../analyze-models/evaluate/roc-curve-tab/cumulative-charts.html)
          * [ Custom charts ](../../analyze-models/evaluate/roc-curve-tab/custom-charts.html)
          * [ Metrics ](../../analyze-models/evaluate/roc-curve-tab/metrics.html)
        * [ Series Insights (clustering) ](../../analyze-models/evaluate/series-insights.html)
        * [ Series Insights (multiseries) ](../../analyze-models/evaluate/series-insights-multi.html)
        * [ Stability ](../../analyze-models/evaluate/stability.html)
        * [ Training Dashboard ](../../analyze-models/evaluate/training-dash.html)
      * [ Understand ](../../analyze-models/understand/index.html) [ Understand ](../../analyze-models/understand/index.html)
        * [ Cluster Insights ](../../analyze-models/understand/cluster-insights.html)
        * [ Feature Effects ](../../analyze-models/understand/feature-effects.html)
        * [ Feature Impact ](../../analyze-models/understand/feature-impact.html)
        * [ Prediction Explanations ](../../analyze-models/understand/pred-explain/index.html) [ Prediction Explanations ](../../analyze-models/understand/pred-explain/index.html)
          * [ Prediction Explanations overview ](../../analyze-models/understand/pred-explain/predex-overview.html)
          * [ SHAP Prediction Explanations ](../../analyze-models/understand/pred-explain/shap-pe.html)
          * [ XEMP Prediction Explanations ](../../analyze-models/understand/pred-explain/xemp-pe.html)
          * [ Text Prediction Explanations ](../../analyze-models/understand/pred-explain/predex-text.html)
          * [ Prediction Explanations for clusters ](../../analyze-models/understand/pred-explain/cluster-pe.html)
          * [ Prediction Explanations for time-aware projects ](../../analyze-models/understand/pred-explain/ts-otv-predex.html)
        * [ Word Cloud ](../../analyze-models/understand/word-cloud.html)
      * [ Describe ](../../analyze-models/describe/index.html) [ Describe ](../../analyze-models/describe/index.html)
        * [ Blueprint ](../../analyze-models/describe/blueprints.html)
        * [ Blueprint JSON ](../../analyze-models/describe/blueprint-json.html)
        * [ Coefficients (preprocessing) ](../../analyze-models/describe/coefficients.html)
        * [ Constraints (monotonic) ](../../analyze-models/describe/monotonic.html)
        * [ Data Quality Handling Report ](../../analyze-models/describe/dq-report.html)
        * [ Eureqa Models ](../../analyze-models/describe/eureqa.html)
        * [ Log ](../../analyze-models/describe/log.html)
        * [ Model Info ](../../analyze-models/describe/model-info.html)
        * [ Rating Tables ](../../analyze-models/describe/rating-table.html)
        * [ GA2M output (from Rating Tables) ](../../analyze-models/describe/ga2m.html)
      * [ Predict ](../../analyze-models/predictions/index.html) [ Predict ](../../analyze-models/predictions/index.html)
        * [ Deploy ](../../analyze-models/predictions/deploy.html)
        * [ Downloads ](../../analyze-models/predictions/download.html)
        * [ Make Predictions ](../../analyze-models/predictions/predict.html)
        * [ Portable Predictions ](../../analyze-models/predictions/port-pred.html)
      * [ Compliance ](../../analyze-models/compliance/index.html) [ Compliance ](../../analyze-models/compliance/index.html)
        * [ Model Compliance ](../../analyze-models/compliance/compliance.html)
        * [ Template Builder for compliance reports ](../../analyze-models/compliance/template-builder.html)
      * [ Comments ](../../analyze-models/comments/index.html)
      * [ Bias and Fairness ](../../analyze-models/bias/index.html) [ Bias and Fairness ](../../analyze-models/bias/index.html)
        * [ Cross-Class Accuracy ](../../analyze-models/bias/cross-acc.html)
        * [ Cross-Class Data Disparity ](../../analyze-models/bias/cross-data.html)
        * [ Per-Class Bias ](../../analyze-models/bias/per-class.html)
      * [ Other ](../../analyze-models/other/index.html) [ Other ](../../analyze-models/other/index.html)
        * [ Bias vs Accuracy ](../../analyze-models/other/bias-tab.html)
        * [ Insights ](../../analyze-models/other/analyze-insights.html)
        * [ Learning Curves ](../../analyze-models/other/learn-curve.html)
        * [ Model Comparison ](../../analyze-models/other/model-compare.html)
        * [ Speed vs Accuracy ](../../analyze-models/other/speed.html)
    * [ Specialized workflows ](../../special-workflows/index.html) [ Specialized workflows ](../../special-workflows/index.html)
      * [ Bias and Fairness resources ](../../special-workflows/bias-resources.html)
      * [ Composable ML ](../../special-workflows/cml/index.html) [ Composable ML ](../../special-workflows/cml/index.html)
        * [ Composable ML overview ](../../special-workflows/cml/cml-overview.html)
        * [ Composable ML Quickstart ](../../special-workflows/cml/cml-quickstart.html)
        * [ Modify a blueprint ](../../special-workflows/cml/cml-blueprint-edit.html)
        * [ Create custom tasks ](../../special-workflows/cml/cml-custom-tasks.html)
        * [ Custom environments ](../../special-workflows/cml/cml-custom-env.html)
        * [ DRUM CLI tool ](../../special-workflows/cml/cml-drum.html)
        * [ Enable network access for custom tasks ](../../special-workflows/cml/custom-task-network-access.html)
      * [ Document AI ](../../special-workflows/doc-ai/index.html) [ Document AI ](../../special-workflows/doc-ai/index.html)
        * [ Document AI overview ](../../special-workflows/doc-ai/doc-ai-overview.html)
        * [ Document ingest and modeling ](../../special-workflows/doc-ai/doc-ai-ingest.html)
        * [ Document AI insights ](../../special-workflows/doc-ai/doc-ai-insights.html)
        * [ Predictions from documents ](../../special-workflows/doc-ai/doc-ai-predictions.html)
      * [ Location AI ](../../special-workflows/location-ai/index.html) [ Location AI ](../../special-workflows/location-ai/index.html)
        * [ Data ingest ](../../special-workflows/location-ai/lai-ingest.html)
        * [ Exploratory Spatial Data Analysis (ESDA) ](../../special-workflows/location-ai/lai-esda.html)
        * [ Modeling ](../../special-workflows/location-ai/lai-model.html)
        * [ Accuracy Over Space ](../../special-workflows/location-ai/lai-insights.html)
      * [ Unsupervised learning ](../../special-workflows/unsupervised/index.html) [ Unsupervised learning ](../../special-workflows/unsupervised/index.html)
        * [ Anomaly detection ](../../special-workflows/unsupervised/anomaly-detection.html)
        * [ Clustering ](../../special-workflows/unsupervised/clustering.html)
      * [ Visual AI ](../../special-workflows/visual-ai/index.html) [ Visual AI ](../../special-workflows/visual-ai/index.html)
        * [ Visual AI overview ](../../special-workflows/visual-ai/vai-overview.html)
        * [ Build Visual AI models ](../../special-workflows/visual-ai/vai-model.html)
        * [ Train-time image augmentation ](../../special-workflows/visual-ai/tti-augment/index.html) [ Train-time image augmentation ](../../special-workflows/visual-ai/tti-augment/index.html)
          * [ About augmented models ](../../special-workflows/visual-ai/tti-augment/ttia-introduction.html)
          * [ Transformations and lists ](../../special-workflows/visual-ai/tti-augment/ttia-lists.html)
          * [ Use case examples ](../../special-workflows/visual-ai/tti-augment/ttia-examples.html)
        * [ Model insights ](../../special-workflows/visual-ai/vai-insights.html)
        * [ Tune models ](../../special-workflows/visual-ai/vai-tuning.html)
        * [ Visual AI predictions ](../../special-workflows/visual-ai/vai-predictions.html)
      * [ Multilabel modeling ](../../special-workflows/multilabel.html)
      * [ Out-of-time validation modeling ](../../special-workflows/otv.html)
      * [ Text AI resources ](../../special-workflows/textai-resources.html)
    * [ Time-series modeling ](../../time/index.html) [ Time-series modeling ](../../time/index.html)
      * [ What is time-aware modeling? ](../../time/whatis-time.html)
      * [ Time series modeling ](../../time/ts-flow-overview.html)
      * [ Time series insights ](../../time/ts-leaderboard.html)
      * [ Time series predictions ](../../time/ts-predictions.html)
      * [ Time series portable predictions with prediction intervals ](../../time/ts-port-pred-intervals.html)
      * [ Multiseries modeling ](../../time/multiseries.html)
      * [ Clustering ](../../time/ts-clustering.html)
      * [ Segmented modeling ](../../time/ts-segmented.html)
      * [ Nowcasting ](../../time/nowcasting.html)
      * [ External prediction comparison ](../../time/cyob.html)
      * [ Batch predictions for TTS and LSTM models ](../../time/ts-tts-lstm-batch-pred.html)
      * [ Time series advanced modeling ](../../time/ts-adv-modeling/index.html) [ Time series advanced modeling ](../../time/ts-adv-modeling/index.html)
        * [ Time series advanced options ](../../time/ts-adv-modeling/ts-adv-opt.html)
        * [ Clustering advanced options ](../../time/ts-adv-modeling/ts-cluster-adv-opt.html)
        * [ Date/time partitioning advanced options ](../../time/ts-adv-modeling/ts-date-time.html)
        * [ Customizing time series projects ](../../time/ts-adv-modeling/ts-customization.html)
      * [ Time series modeling data ](../../time/ts-modeling-data/index.html) [ Time series modeling data ](../../time/ts-modeling-data/index.html)
        * [ Create the modeling dataset ](../../time/ts-modeling-data/ts-create-data.html)
        * [ Data prep for time series ](../../time/ts-modeling-data/ts-data-prep.html)
        * [ Restore features removed by reduction ](../../time/ts-modeling-data/restore-features.html)
    * [ AutoML preview features ](../../automl-preview/index.html) [ AutoML preview features ](../../automl-preview/index.html)
      * [ Quantile regression analysis ](../../automl-preview/quantile-reg.html)
      * [ Configure hyperparameters for custom tasks ](../../automl-preview/cml-hyperparam.html)
    * [ Modeling FAQ ](../../general-modeling-faq.html)
    * [ Value Tracker ](../../value-tracker.html)
    * [ Project control center ](../../manage-projects.html)
  * [ Predictions ](../../../predictions/index.html) [ Predictions ](../../../predictions/index.html)
    * [ Real-time scoring methods ](../../../predictions/realtime/index.html) [ Real-time scoring methods ](../../../predictions/realtime/index.html)
      * [ Prediction API snippets ](../../../predictions/realtime/code-py.html)
      * [ Qlik predictions ](../../../predictions/realtime/integration-code-snippets.html)
    * [ Batch prediction methods ](../../../predictions/batch/index.html) [ Batch prediction methods ](../../../predictions/batch/index.html)
      * [ Batch prediction UI ](../../../predictions/batch/batch-dep/index.html) [ Batch prediction UI ](../../../predictions/batch/batch-dep/index.html)
        * [ Make a one-time batch prediction ](../../../predictions/batch/batch-dep/batch-pred.html)
        * [ Schedule recurring batch prediction jobs ](../../../predictions/batch/batch-dep/batch-pred-jobs.html)
        * [ Manage prediction job definitions ](../../../predictions/batch/batch-dep/manage-pred-job-def.html)
        * [ Snowflake prediction job examples ](../../../predictions/batch/batch-dep/pred-job-examples-snowflake.html)
      * [ Prediction monitoring jobs ](../../../predictions/batch/pred-monitoring-jobs/index.html) [ Prediction monitoring jobs ](../../../predictions/batch/pred-monitoring-jobs/index.html)
        * [ Create monitoring jobs ](../../../predictions/batch/pred-monitoring-jobs/ui-monitoring-jobs.html)
        * [ Monitoring jobs API ](../../../predictions/batch/pred-monitoring-jobs/api-monitoring-jobs.html)
        * [ Manage monitoring job definitions ](../../../predictions/batch/pred-monitoring-jobs/manage-monitoring-job-def.html)
      * [ Manage batch jobs ](../../../predictions/batch/batch-jobs.html)
      * [ Batch prediction scripts ](../../../predictions/batch/cli-scripts.html)
    * [ Portable prediction methods ](../../../predictions/port-pred/index.html) [ Portable prediction methods ](../../../predictions/port-pred/index.html)
      * [ Scoring Code ](../../../predictions/port-pred/scoring-code/index.html) [ Scoring Code ](../../../predictions/port-pred/scoring-code/index.html)
        * [ Download Scoring Code from the Leaderboard ](../../../predictions/port-pred/scoring-code/sc-download-leaderboard.html)
        * [ Download Scoring Code from a deployment ](../../../predictions/port-pred/scoring-code/sc-download-deployment.html)
        * [ Download Scoring Code from the Leaderboard (Legacy) ](../../../predictions/port-pred/scoring-code/sc-download-legacy.html)
        * [ Scoring Code for time series projects ](../../../predictions/port-pred/scoring-code/sc-time-series.html)
        * [ Scoring at the command line ](../../../predictions/port-pred/scoring-code/scoring-cli.html)
        * [ Scoring Code usage examples ](../../../predictions/port-pred/scoring-code/quickstart-api.html)
        * [ JAR structure ](../../../predictions/port-pred/scoring-code/jar-package.html)
        * [ Generate Java models in an existing project ](../../../predictions/port-pred/scoring-code/build-verify.html)
        * [ Backward-compatible Java API ](../../../predictions/port-pred/scoring-code/java-back-compat.html)
        * [ Scoring Code JAR integrations ](../../../predictions/port-pred/scoring-code/sc-jar-integrations.html)
        * [ Android integration ](../../../predictions/port-pred/scoring-code/android.html)
      * [ Portable Prediction Server ](../../../predictions/port-pred/pps/index.html) [ Portable Prediction Server ](../../../predictions/port-pred/pps/index.html)
        * [ Portable Prediction Server configuration ](../../../predictions/port-pred/pps/portable-pps.html)
        * [ Portable Prediction Server running modes ](../../../predictions/port-pred/pps/pps-run-modes.html)
        * [ Portable batch predictions ](../../../predictions/port-pred/pps/portable-batch-predictions.html)
        * [ Custom model Portable Prediction Server ](../../../predictions/port-pred/pps/custom-pps.html)
      * [ DataRobot Prime (deprecated) ](../../../predictions/port-pred/prime/index.html)
    * [ Predictions testing ](../../../predictions/pred-test.html)
    * [ Predictions reference ](../../../predictions/pred-file-limits.html)
  * [ MLOps ](../../../mlops/index.html) [ MLOps ](../../../mlops/index.html)
    * [ Deployment ](../../../mlops/deployment/index.html) [ Deployment ](../../../mlops/deployment/index.html)
      * [ Deployment workflows ](../../../mlops/deployment/deploy-workflows/index.html) [ Deployment workflows ](../../../mlops/deployment/deploy-workflows/index.html)
        * [ DataRobot model in a DataRobot environment ](../../../mlops/deployment/deploy-workflows/dr-model-dr-env.html)
        * [ DataRobot model in a PPS ](../../../mlops/deployment/deploy-workflows/dr-model-pps-env.html)
        * [ Custom model in a DataRobot environment ](../../../mlops/deployment/deploy-workflows/cus-model-dr-env.html)
        * [ Custom model in a PPS ](../../../mlops/deployment/deploy-workflows/cus-model-pps-env.html)
        * [ Scoring Code in an external environment ](../../../mlops/deployment/deploy-workflows/ext-dr-model-ext-env.html)
        * [ Monitor an external model with the monitoring agent ](../../../mlops/deployment/deploy-workflows/ext-cus-model-ext-env.html)
      * [ Register models ](../../../mlops/deployment/registry/index.html) [ Register models ](../../../mlops/deployment/registry/index.html)
        * [ Model Registry ](../../../mlops/deployment/registry/reg-create.html)
        * [ Register DataRobot models ](../../../mlops/deployment/registry/dr-model-reg.html)
        * [ Register custom models ](../../../mlops/deployment/registry/reg-custom-models.html)
        * [ Register external models ](../../../mlops/deployment/registry/reg-external-models.html)
        * [ Deploy registered models ](../../../mlops/deployment/registry/reg-deploy.html)
        * [ View and manage registered models ](../../../mlops/deployment/registry/reg-action.html)
        * [ Generate model compliance documentation ](../../../mlops/deployment/registry/reg-compliance.html)
        * [ Extend compliance documentation with key values ](../../../mlops/deployment/registry/reg-key-values.html)
        * [ Custom jobs ](../../../mlops/deployment/registry/reg-custom-jobs.html)
        * [ Import model packages into MLOps ](../../../mlops/deployment/registry/reg-transfer.html)
        * [ Model logs for model packages (legacy) ](../../../mlops/deployment/registry/reg-model-pkg-logs.html)
      * [ Prepare custom models for deployment ](../../../mlops/deployment/custom-models/index.html) [ Prepare custom models for deployment ](../../../mlops/deployment/custom-models/index.html)
        * [ Custom Model Workshop ](../../../mlops/deployment/custom-models/custom-model-workshop/index.html) [ Custom Model Workshop ](../../../mlops/deployment/custom-models/custom-model-workshop/index.html)
          * [ Create custom inference models ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-inf-model.html)
          * [ Manage custom model dependencies ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-model-dependencies.html)
          * [ Manage custom model resources ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-model-resource-mgmt.html)
          * [ Add custom model versions ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-model-versions.html)
          * [ Add training data to a custom model ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-model-training-data.html)
          * [ Add files from remote repos to custom models ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-model-repos.html)
          * [ Test custom models ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-model-test.html)
          * [ Manage custom models ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-model-actions.html)
          * [ Register custom models ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-model-reg.html)
          * [ Create custom model proxies for external models ](../../../mlops/deployment/custom-models/custom-model-workshop/ext-model-proxy.html)
          * [ GitHub Actions for custom models ](../../../mlops/deployment/custom-models/custom-model-workshop/custom-model-github-action.html)
        * [ Custom model environments ](../../../mlops/deployment/custom-models/custom-model-environments/index.html) [ Custom model environments ](../../../mlops/deployment/custom-models/custom-model-environments/index.html)
          * [ Drop-in environments ](../../../mlops/deployment/custom-models/custom-model-environments/drop-in-environments.html)
          * [ Custom environments ](../../../mlops/deployment/custom-models/custom-model-environments/custom-environments.html)
      * [ Prepare for external model deployment ](../../../mlops/deployment/ext-model-prep/index.html) [ Prepare for external model deployment ](../../../mlops/deployment/ext-model-prep/index.html)
        * [ Add external prediction environments ](../../../mlops/deployment/ext-model-prep/ext-pred-env.html)
        * [ Manage prediction environments ](../../../mlops/deployment/ext-model-prep/ext-pred-env-manage.html)
        * [ Register external models ](../../../mlops/deployment/ext-model-prep/ext-model-reg.html)
      * [ Manage prediction environments ](../../../mlops/deployment/prediction-env/index.html) [ Manage prediction environments ](../../../mlops/deployment/prediction-env/index.html)
        * [ Add DataRobot Serverless prediction environments ](../../../mlops/deployment/prediction-env/pred-env.html)
        * [ Add external prediction environments ](../../../mlops/deployment/prediction-env/ext-pred-env.html)
        * [ Manage prediction environments ](../../../mlops/deployment/prediction-env/pred-env-manage.html)
        * [ Deploy a model to a prediction environment ](../../../mlops/deployment/prediction-env/pred-env-deploy.html)
        * [ Prediction environment integrations ](../../../mlops/deployment/prediction-env/pred-env-integrations/index.html) [ Prediction environment integrations ](../../../mlops/deployment/prediction-env/pred-env-integrations/index.html)
          * [ Automated deployment and replacement of Scoring Code in AzureML ](../../../mlops/deployment/prediction-env/pred-env-integrations/azureml-sc-deploy-replace.html)
          * [ Automated deployment and replacement in Sagemaker ](../../../mlops/deployment/prediction-env/pred-env-integrations/sagemaker-cm-deploy-replace.html)
      * [ Deploy models ](../../../mlops/deployment/deploy-methods/index.html) [ Deploy models ](../../../mlops/deployment/deploy-methods/index.html)
        * [ Deploy DataRobot models ](../../../mlops/deployment/deploy-methods/deploy-model.html)
        * [ Deploy custom models ](../../../mlops/deployment/deploy-methods/deploy-custom-inf-model.html)
        * [ Deploy external models ](../../../mlops/deployment/deploy-methods/deploy-external-model.html)
        * [ Configure deployment settings ](../../../mlops/deployment/deploy-methods/add-deploy-info.html)
        * [ Add prediction data post-deployment ](../../../mlops/deployment/deploy-methods/add-prediction-data-post-deploy.html)
      * [ MLOps agents ](../../../mlops/deployment/mlops-agent/index.html) [ MLOps agents ](../../../mlops/deployment/mlops-agent/index.html)
        * [ Monitoring agent ](../../../mlops/deployment/mlops-agent/monitoring-agent/index.html) [ Monitoring agent ](../../../mlops/deployment/mlops-agent/monitoring-agent/index.html)
          * [ Installation and configuration ](../../../mlops/deployment/mlops-agent/monitoring-agent/agent.html)
          * [ Examples directory ](../../../mlops/deployment/mlops-agent/monitoring-agent/agent-ex.html)
          * [ Monitoring agent use cases ](../../../mlops/deployment/mlops-agent/monitoring-agent/agent-use.html)
          * [ Environment variables ](../../../mlops/deployment/mlops-agent/monitoring-agent/env-var.html)
          * [ Library and agent spooler configuration ](../../../mlops/deployment/mlops-agent/monitoring-agent/spooler.html)
          * [ Download Scoring Code ](../../../mlops/deployment/mlops-agent/monitoring-agent/agent-sc.html)
          * [ Monitoring external multiclass deployments ](../../../mlops/deployment/mlops-agent/monitoring-agent/agent-multi.html)
        * [ Management agent ](../../../mlops/deployment/mlops-agent/mgmt-agent/index.html) [ Management agent ](../../../mlops/deployment/mlops-agent/mgmt-agent/index.html)
          * [ Installation and configuration ](../../../mlops/deployment/mlops-agent/mgmt-agent/mgmt-agent-install.html)
          * [ Configure environment plugins ](../../../mlops/deployment/mlops-agent/mgmt-agent/mgmt-agent-plugins.html)
          * [ Install the management agent for Kubernetes ](../../../mlops/deployment/mlops-agent/mgmt-agent/mgmt-agent-kubernetes.html)
          * [ Management agent deployment status and events ](../../../mlops/deployment/mlops-agent/mgmt-agent/mgmt-agent-events-status.html)
          * [ Relaunch deployments ](../../../mlops/deployment/mlops-agent/mgmt-agent/mgmt-agent-relaunch.html)
          * [ Force delete deployments ](../../../mlops/deployment/mlops-agent/mgmt-agent/mgmt-agent-delete.html)
        * [ Agent event log ](../../../mlops/deployment/mlops-agent/agent-event-log.html)
    * [ Deployment settings ](../../../mlops/deployment-settings/index.html) [ Deployment settings ](../../../mlops/deployment-settings/index.html)
      * [ Set up service health monitoring ](../../../mlops/deployment-settings/service-health-settings.html)
      * [ Set up data drift monitoring ](../../../mlops/deployment-settings/data-drift-settings.html)
      * [ Set up accuracy monitoring ](../../../mlops/deployment-settings/accuracy-settings.html)
      * [ Set up fairness monitoring ](../../../mlops/deployment-settings/fairness-settings.html)
      * [ Set up humility rules ](../../../mlops/deployment-settings/humility-settings.html)
      * [ Configure retraining ](../../../mlops/deployment-settings/retraining-settings.html)
      * [ Configure challengers ](../../../mlops/deployment-settings/challengers-settings.html)
      * [ Configure predictions settings ](../../../mlops/deployment-settings/predictions-settings.html)
      * [ Enable data exploration ](../../../mlops/deployment-settings/data-exploration-settings.html)
      * [ Set up custom metrics monitoring ](../../../mlops/deployment-settings/custom-metrics-settings.html)
      * [ Set up timeliness tracking ](../../../mlops/deployment-settings/usage-settings.html)
    * [ Lifecycle management ](../../../mlops/manage-mlops/index.html) [ Lifecycle management ](../../../mlops/manage-mlops/index.html)
      * [ Deployment inventory ](../../../mlops/manage-mlops/deploy-inventory.html)
      * [ Manage deployments ](../../../mlops/manage-mlops/actions-menu.html)
      * [ Replace deployed models ](../../../mlops/manage-mlops/deploy-replace.html)
      * [ Manage Automated Retraining policies ](../../../mlops/manage-mlops/set-up-auto-retraining.html)
    * [ Performance monitoring ](../../../mlops/monitor/index.html) [ Performance monitoring ](../../../mlops/monitor/index.html)
      * [ Overview tab ](../../../mlops/monitor/dep-overview.html)
      * [ Accuracy tab ](../../../mlops/monitor/deploy-accuracy.html)
      * [ Data Drift tab ](../../../mlops/monitor/data-drift.html)
      * [ Service Health tab ](../../../mlops/monitor/service-health.html)
      * [ Challengers tab ](../../../mlops/monitor/challengers.html)
      * [ Usage tab ](../../../mlops/monitor/deploy-usage.html)
      * [ Data Exploration tab ](../../../mlops/monitor/data-exploration.html)
      * [ Custom Metrics tab ](../../../mlops/monitor/custom-metrics.html)
      * [ Segmented analysis ](../../../mlops/monitor/deploy-segment.html)
      * [ Batch monitoring ](../../../mlops/monitor/deploy-batch-monitor.html)
      * [ Generative model monitoring ](../../../mlops/monitor/generative-model-monitoring.html)
    * [ Governance ](../../../mlops/governance/index.html) [ Governance ](../../../mlops/governance/index.html)
      * [ Model deployment approval workflow ](../../../mlops/governance/dep-admin.html)
      * [ Governance lens ](../../../mlops/governance/gov-lens.html)
      * [ Notifications tab ](../../../mlops/governance/deploy-notifications.html)
      * [ Humility tab ](../../../mlops/governance/humble.html)
      * [ Fairness tab ](../../../mlops/governance/mlops-fairness.html)
      * [ Deployment reports ](../../../mlops/governance/deploy-reports.html)
    * [ MLOps preview features ](../../../mlops/mlops-preview/index.html) [ MLOps preview features ](../../../mlops/mlops-preview/index.html)
      * [ Service Health and Accuracy history ](../../../mlops/mlops-preview/pp-deploy-history.html)
      * [ Automated deployment and replacement of Scoring Code in Snowflake ](../../../mlops/mlops-preview/pp-snowflake-sc-deploy-replace.html)
      * [ Run the monitoring agent in DataRobot ](../../../mlops/mlops-preview/monitoring-agent-in-dr.html)
      * [ Feature cache for Feature Discovery deployments ](../../../mlops/mlops-preview/safer-ft-cache.html)
      * [ MLOps reporting for unstructured models ](../../../mlops/mlops-preview/mlops-unstructured-models.html)
    * [ MLOps FAQ ](../../../mlops/mlops-faq.html)
  * [ Notebooks ](../../../dr-notebooks/index.html) [ Notebooks ](../../../dr-notebooks/index.html)
    * [ Manage notebooks ](../../../dr-notebooks/manage-nb/index.html) [ Manage notebooks ](../../../dr-notebooks/manage-nb/index.html)
      * [ Add notebooks ](../../../dr-notebooks/manage-nb/dr-create-nb.html)
      * [ Notebook settings ](../../../dr-notebooks/manage-nb/dr-settings-nb.html)
      * [ Notebook versioning ](../../../dr-notebooks/manage-nb/dr-revise-nb.html)
    * [ Notebook coding experience ](../../../dr-notebooks/code-nb/index.html) [ Notebook coding experience ](../../../dr-notebooks/code-nb/index.html)
      * [ Environment management ](../../../dr-notebooks/code-nb/dr-env-nb.html)
      * [ Create and execute cells ](../../../dr-notebooks/code-nb/dr-cell-nb.html)
      * [ Cell actions ](../../../dr-notebooks/code-nb/dr-action-nb.html)
      * [ Code intelligence ](../../../dr-notebooks/code-nb/dr-code-int.html)
      * [ Notebook terminals ](../../../dr-notebooks/code-nb/dr-terminal-nb.html)
      * [ Azure OpenAI Service integration ](../../../dr-notebooks/code-nb/dr-openai-nb.html)
    * [ Notebook reference ](../../../dr-notebooks/dr-notebook-ref.html)
  * [ AI Apps ](../../../app-builder/index.html) [ AI Apps ](../../../app-builder/index.html)
    * [ Create applications ](../../../app-builder/create-app.html)
    * [ Manage applications ](../../../app-builder/current-app.html)
    * [ Edit no-code applications ](../../../app-builder/edit-apps/index.html) [ Edit no-code applications ](../../../app-builder/edit-apps/index.html)
      * [ Pages ](../../../app-builder/edit-apps/app-pages.html)
      * [ Widgets ](../../../app-builder/edit-apps/app-widgets.html)
      * [ What-if and Optimizer ](../../../app-builder/edit-apps/whatif-opt.html)
      * [ Settings ](../../../app-builder/edit-apps/app-settings.html)
    * [ Use no-code applications ](../../../app-builder/use-apps/index.html) [ Use no-code applications ](../../../app-builder/use-apps/index.html)
      * [ Make predictions ](../../../app-builder/use-apps/app-make-pred.html)
      * [ View prediction results ](../../../app-builder/use-apps/app-analyze-result.html)
    * [ Time series applications ](../../../app-builder/ts-app.html)
    * [ Custom apps ](../../../app-builder/custom-apps/index.html) [ Custom apps ](../../../app-builder/custom-apps/index.html)
      * [ Upload custom applications ](../../../app-builder/custom-apps/app-upload-custom.html)
      * [ Host custom applications ](../../../app-builder/custom-apps/custom-apps-hosting.html)
      * [ Manage custom applications ](../../../app-builder/custom-apps/manage-custom-apps.html)
    * [ AI App reference ](../../../app-builder/reference/index.html) [ AI App reference ](../../../app-builder/reference/index.html)
      * [ Default widgets ](../../../app-builder/reference/default-widgets.html)
      * [ Optional widgets ](../../../app-builder/reference/optional-widgets.html)
    * [ AI App preview features ](../../../app-builder/app-preview/index.html) [ AI App preview features ](../../../app-builder/app-preview/index.html)
      * [ Prefill application templates ](../../../app-builder/app-preview/app-prefill.html)
      * [ Feature Discovery support in No-Code AI Apps ](../../../app-builder/app-preview/app-ft-cache.html)
  * [ Integrations ](../../../integrations/index.html) [ Integrations ](../../../integrations/index.html)
    * [ AWS ](../../../integrations/aws/index.html) [ AWS ](../../../integrations/aws/index.html)
      * [ Import data from AWS S3 ](../../../integrations/aws/import-from-aws-s3.html)
      * [ Deploy models on AWS EKS ](../../../integrations/aws/deploy-dr-models-on-aws.html)
      * [ Path-based routing to PPS ](../../../integrations/aws/path-based-routing-to-pps-on-aws.html)
      * [ Score Snowflake data on AWS EMR Spark ](../../../integrations/aws/score-snowflake-aws-emr-spark.html)
      * [ Ingest data with AWS Athena ](../../../integrations/aws/ingest-athena.html)
      * [ AWS Lambda ](../../../integrations/aws/lambda/index.html) [ AWS Lambda ](../../../integrations/aws/lambda/index.html)
        * [ AWS Lambda reporting to MLOps ](../../../integrations/aws/lambda/aws-lambda-reporting-to-mlops.html)
        * [ Use DataRobot Prime models with AWS Lambda ](../../../integrations/aws/lambda/prime-lambda.html)
        * [ Use Scoring Code with AWS Lambda ](../../../integrations/aws/lambda/sc-lambda.html)
      * [ Amazon SageMaker ](../../../integrations/aws/sagemaker/index.html) [ Amazon SageMaker ](../../../integrations/aws/sagemaker/index.html)
        * [ Deploy models on SageMaker ](../../../integrations/aws/sagemaker/sagemaker-deploy.html)
        * [ Use Scoring Code with AWS SageMaker ](../../../integrations/aws/sagemaker/sc-sagemaker.html)
    * [ Azure ](../../../integrations/azure/index.html) [ Azure ](../../../integrations/azure/index.html)
      * [ Run Batch Prediction jobs from Azure Blob Storage ](../../../integrations/azure/azure-blob-storage-batch-pred.html)
      * [ Deploy and monitor DataRobot models in Azure Kubernetes Service ](../../../integrations/azure/aks-deploy-and-monitor.html)
      * [ Deploy and monitor Spark models with DataRobot MLOps ](../../../integrations/azure/spark-deploy-and-monitor.html)
      * [ Deploy and monitor ML.NET models with DataRobot MLOps ](../../../integrations/azure/mlnet-deploy-and-monitor.html)
      * [ Use Scoring Code with Azure ML ](../../../integrations/azure/sc-azureml.html)
    * [ Google ](../../../integrations/google/index.html) [ Google ](../../../integrations/google/index.html)
      * [ Deploy and monitor models on GCP ](../../../integrations/google/google-cloud-platform.html)
      * [ Deploy the MLOps agent on GKE ](../../../integrations/google/mlops-agent-with-gke.html)
    * [ Snowflake ](../../../integrations/snowflake/index.html) [ Snowflake ](../../../integrations/snowflake/index.html)
      * [ Data ingest and project creation ](../../../integrations/snowflake/sf-project-creation.html)
      * [ Real-time predictions ](../../../integrations/snowflake/sf-client-scoring.html)
      * [ Server-side model scoring ](../../../integrations/snowflake/sf-server-scoring.html)
      * [ Snowflake external functions and streams ](../../../integrations/snowflake/sf-function-streams.html)
      * [ Generate Snowflake UDF Scoring Code ](../../../integrations/snowflake/snowflake-sc.html)

[For Self-Managed AI Platform users running v11.1, see the on-premise platform
documentation __](/11.1/en/docs/index.html)

Bias and Fairness

  * Configure metrics and mitigation pre-Autopilot 
    * Set fairness metrics 
    * Set mitigation techniques 
  * Configure metrics and mitigation post-Autopilot 
    * Retrain with fairness tests 
    * Retrain with mitigation 
      * Single-model retraining 
      * Multiple-model retraining 
    * Identify mitigated models 
    * Compare models 
  * Mitigation eligibility 
  * Bias mitigation considerations 

[Modeling](../../index.html "Modeling") > [Build models](../index.html "Build
models") > [Advanced options](index.html "Advanced options") > Bias and
Fairness

# Bias and Fairness¶

Bias and Fairness testing provides methods to calculate fairness for a binary
classification model and attempt to identify any biases in the model's
predictive behavior. In DataRobot, bias represents the difference between a
model's predictions for different populations (or groups) while fairness is
the measure of the model's bias.

Select protected features in the dataset and choose fairness metrics and
mitigation techniques either before model building or from the Leaderboard
once models are built. [Bias and Fairness insights](../../analyze-
models/bias/index.html) help identify bias in a model and visualize the root-
cause analysis, explaining why the model is learning bias from the training
data and from where.

Bias mitigation in DataRobot is a technique for reducing (“mitigating”) model
bias for an identified [protected
feature](../../../reference/glossary/index.html#protected-feature)—by
producing predictions with higher scores on a selected fairness metric for one
or more groups (classes) in a protected feature. It is available for binary
classification projects, and typically results in a small reduction in
accuracy in exchange for greater fairness.

See the [Bias and Fairness](../../special-workflows/bias-resources.html)
resource page for more complete information on the generally available bias
and fairness testing and mitigation capabilities.

## Configure metrics and mitigation pre-Autopilot¶

Once you select a target, click **Show advanced options** and select the
**Bias and Fairness** tab. From the tab you can set fairness metrics and
mitigation techniques.

[![](../../../images/bias-mit-1.png)](../../../images/bias-mit-1.png)

### Set fairness metrics¶

To configure **Bias and Fairness** , set the values that define your use case.
For additional detail, refer to the [bias and fairness
reference](../../../reference/pred-ai-ref/bias-ref.html) for common terms and
metric definitions.

[![](../../../images/bias-and-fairness-1.png)](../../../images/bias-and-
fairness-1.png)

  1. Identify up to 10 **Protected Features** in the dataset. Protected features must be categorical. The model's fairness is calculated against the protected features selected from the dataset.

[![](../../../images/bias-and-fairness-2.png)](../../../images/bias-and-
fairness-2.png)

  2. Define the **Favorable Target Outcome** , i.e., the outcome perceived as favorable for the protected class relative to the target. In the below example, the target is "salary" so annual salaries are listed under Favorable Target Outcome, and a favorable outcome is earning greater than 50K.

[![](../../../images/bias-and-fairness-3.png)](../../../images/bias-and-
fairness-3.png)

  3. Choose the **Primary Fairness Metric** most appropriate for your use case from the five options below.

Help me choose

If you are unsure of the best metric for your model, click **Help me choose**.

[![](../../../images/bias-and-fairness-10.png)](../../../images/bias-and-
fairness-10.png)

DataRobot presents a questionnaire where each question is determined by your
answer to the previous one. Once completed, DataRobot recommends a metric
based on your answers.

[![](../../../images/bias-and-fairness-5.png)](../../../images/bias-and-
fairness-5.png)

Because bias and fairness are ethically complex, DataRobot's questions cannot
capture every detail of each use case. Use the recommended metric as a
guidepost; it is not necessarily the correct (or only) metric appropriate for
your use case. Select different metrics to observe how answering the questions
differently would affect the recommendation.

Click **Select** to add the highlighted option to the **Primary Fairness
Metric** field.

Metric | Description  
---|---  
[Proportional Parity](../../../reference/pred-ai-ref/bias-ref.html#proportional-parity) | For each protected class, what is the probability of receiving favorable predictions from the model? This metric (also known as "Statistical Parity" or "Demographic Parity") is based on equal representation of the model's target across protected classes.  
[Equal Parity](../../../reference/pred-ai-ref/bias-ref.html#equal-parity) | For each protected class, what is the total number of records with favorable predictions from the model? This metric is based on equal representation of the model's target across protected classes.  
Prediction Balance ([Favorable Class Balance](../../../reference/pred-ai-ref/bias-ref.html#favorable-class-balance) and [Unfavorable Class Balance](../../../reference/pred-ai-ref/bias-ref.html#unfavorable-class-balance)) | For all actuals that were favorable/unfavorable outcomes, what is the average predicted probability for each protected class? This metric is based on equal representation of the model's average raw scores across each protected class and is part of the set of Prediction Balance fairness metrics.  
[True Favorable Rate Parity](../../../reference/pred-ai-ref/bias-ref.html#true-favorable-rate-parity) and [True Unfavorable Rate Parity](../../../reference/pred-ai-ref/bias-ref.html#true-unfavorable-rate-parity) | For each protected class, what is the probability of the model predicting the favorable/unfavorable outcome for all actuals of the favorable/unfavorable outcome? This metric is based on equal error.  
[Favorable Predictive Value Parity](../../../reference/pred-ai-ref/bias-ref.html#favorable-predictive-value-parity) and [Unfavorable Predictive Value Parity](../../../reference/pred-ai-ref/bias-ref.html#unfavorable-predictive-value-parity) | What is the probability of the model being correct (i.e., the actual results being favorable/unfavorable)? This metric (also known as "Positive Predictive Value Parity") is based on equal error.  
  
[![](../../../images/bias-and-fairness-4.png)](../../../images/bias-and-
fairness-4.png)

The fairness metric serves as the foundation for the calculated fairness
score; a numerical computation of the model's fairness against the protected
class.

  4. Set a **Fairness Threshold** for the project. The threshold serves as a benchmark for the model's fairness score. That is, it measures if a model performs within appropriate fairness bounds for each protected class. It does not affect the fairness score or performance of any protected class. (See the [reference section](../../../reference/pred-ai-ref/bias-ref.html) for more information.)

[![](../../../images/bias-and-fairness-11.png)](../../../images/bias-and-
fairness-11.png)

### Set mitigation techniques¶

[![](../../../images/bias-mit-1a.png)](../../../images/bias-mit-1a.png)

Select a bias mitigation technique for DataRobot to apply automatically.
DataRobot uses the selected technique to automatically attempt bias mitigation
for the top three full or Comprehensive Autopilot Leaderboard models (based on
accuracy). You can also initiate bias mitigation manually after Autopilot
completes. (If you used [Quick Autopilot mode](../../../reference/pred-ai-
ref/model-ref.html#quick-autopilot), for example, manual mode allows you to
apply mitigation to selected models). With either method, once applied, you
can compare mitigated versus unmitigated models.

How does mitigation work?

Specifically, mitigation copies an affected blueprint and then adds either a
pre- or post-processing task, depending on the **Mitigation technique**
selected.

[![](../../../images/bias-mit-11.png)](../../../images/bias-mit-11.png)

The table below summarizes the fields:

Field | Description  
---|---  
Bias mitigation feature | Lists the protected feature(s); select one from which to reduce the model's bias towards.  
Include as a predictor variable | Sets whether to include the mitigation feature as an input to model training.  
Bias mitigation technique | Sets the mitigation technique and the point in model processing when mitigation is applied.  
  
The steps below provide greater detail for each field:

  1. Select a feature from the **Bias mitigation feature** dropdown, which lists the feature(s) that you set as protected in the **Protected features** field for general Bias and Fairness settings. This is the feature you would like to reduce the model’s bias towards.

[![](../../../images/bias-mit-2.png)](../../../images/bias-mit-2.png)

  2. Once the mitigation feature is set, DataRobot computes data quality for the feature. When the check is successful, the option to include the protected feature as a predictor variable becomes available. Check the box to use the feature to attempt mitigation and to include the mitigation feature as an input into model training. Leave it unchecked to use the feature for mitigation only, not as a training input. This can be useful when you are legally prohibited from, or don't want to, include sensitive data as a model input but you would like to attempt mitigation based on it.

What does the data quality check identify?

During the data quality check, there are three basic questions answered for
the chosen mitigation feature and the chosen target:

     1. Does the mitigation feature have too many rows where the value is completely missing?
     2. Are there any values of the mitigation feature that are too rare to allow drawing firm conclusions? For example, consider a dataset with 10,000 rows where the mitigated feature is `race`. One of the values, `Inuit`, occurs only seven times, making the sample too small to be representative.
     3. Are there any combinations of class plus target that are rare or absent? For example, consider a mitigation feature of `gender`. The categories `Male` and `Female` are both numerous, but the positive target label never occurs in `Female` rows.

If the quality check does not pass, a warning appears. Address the issues in
the dataset, then re-upload and try again.

  3. Set the **Mitigation technique** , either:

     * _Preprocessing Reweighing:_ Assigns row-level weights and uses those as a special model input during training to attempt to make the predictions more fair.
     * _Postprocessing with Rejection Option-based Classification (ROBC):_ Changes the predicted label for rows that are close to the prediction threshold (model predictions with the highest uncertainty). Read a general ROBC description [here](https://medium.com/towards-data-science/reducing-ai-bias-with-rejection-option-based-classification-54fefdb53c2e) and see a coding example [in this Google Colab notebook](https://colab.research.google.com/github/sony/nnabla-examples/blob/master/interactive-demos/rejection_option_based_classification.ipynb). However, for detailed explanations of the applied algorithms, open the model documentation by clicking on the mitigation method task in the model [blueprin](../../../workbench/wb-experiment/experiment-insights/ml-blueprint.html).
Which fairness metrics does each mitigation techniques use?

The mitigation technique names, "pre" and "post," refer to the point in the
workflow (as illustrated in the blueprint) where the technique is applied. For
example, reweighing is called "preprocessing" because it happens before the
model is trained. Rejection Option-based Classification is called post-
processing because it happens after the model has been trained. The techniques
use the following metrics.

Technique | Metric  
---|---  
Preprocessing Reweighing | Primarily [Proportional Parity](../../../reference/pred-ai-ref/bias-ref.html#proportional-parity) (but may, tangentially, improve other fairness metrics).  
Postprocessing with Rejection Option-based Classification | Proportional Parity and [True Favorable](../../../reference/pred-ai-ref/bias-ref.html#true-favorable-rate-parity) and [True Unfavorable](../../../reference/pred-ai-ref/bias-ref.html#true-unfavorable-rate-parity) Rate Parity  
  4. Start the model building process. DataRobot automatically attempts mitigation on the top three _eligible_ models produced by Autopilot against the **Bias mitigation feature**. Mitigated models can be identified by the BIAS MITIGATION badge on the Leaderboard. See the explanation of what makes a model eligible for mitigation, as well as a table listing ineligible models.

[![](../../../images/bias-mit-3.png)](../../../images/bias-mit-3.png)

  5. Compare bias and accuracy of mitigated vs. unmitigated models.

## Configure metrics and mitigation post-Autopilot¶

If you did not configure **Bias and Fairness** prior to model building, you
can configure fairness tests and mitigation techniques from the Leaderboard.

### Retrain with fairness tests¶

The following describes applying fairness metrics to models after Autopilot
completes.

  1. Select a model and click **Bias and Fairness > Settings**.

[![](../../../images/bias-index-1.png)](../../../images/bias-index-1.png)

  2. Follow the advanced options instructions on configuring bias and fairness.

  3. Click **Save**. DataRobot then configures fairness testing for all models in your project based on these settings.

### Retrain with mitigation¶

After Autopilot has finished, you can apply mitigation to any models that have
not already been mitigated. To do so, select one or multiple model(s) from the
Leaderboard and retrain them with bias mitigation settings applied.

Note

While you cannot retrain an already mitigated model, even on a different
protected feature, you can return to the parent and select a different feature
or technique for mitigation.

From the parent model, you can view the **Models with Mitigation Applied**
table. This table lists relationships between the parent model and any child
models with mitigation applied. Note the parent model does _not_ have
mitigation applied (1). All child mitigated models are listed by model ID (2),
including their mitigation settings.

[![](../../../images/bias-mit-13.png)](../../../images/bias-mit-13.png)

#### Single-model retraining¶

Note

If you haven't previously completed the Bias and Fairness configuration in
advanced options prior to model building, you must first set those fields via
the **Bias and Fairness > Settings** tab.

To apply mitigation to a single Leaderboard model after Autopilot completes:

  1. Expand any eligible Leaderboard model and open **Bias and Fairness > Bias Mitigation**.

[![](../../../images/bias-mit-10.png)](../../../images/bias-mit-10.png)

  2. Configure the fields for bias mitigation.

  3. Click **Apply** to start building a new, mitigated version of the model. When training is complete, the model can be identified on the Leaderboard by the BIAS MITIGATION badge.

  4. Compare bias and accuracy of mitigated vs. unmitigated models.

#### Multiple-model retraining¶

To apply mitigation to multiple Leaderboard models after Autopilot completes:

  1. Use the checkboxes to the left of any eligible models that have not already been mitigated.

  2. From the menu, select **Model processing > Apply bias mitigation for selected models**.

[![](../../../images/bias-mit-4.png)](../../../images/bias-mit-4.png)

  3. In the resulting window, configure the fields for bias mitigation.

[![](../../../images/bias-mit-5.png)](../../../images/bias-mit-5.png)

  4. Click **Apply** to start building new, mitigated versions of the models. When training is complete, the models can be identified on the Leaderboard by the BIAS MITIGATION badge.

  5. Compare bias and accuracy of mitigated vs. unmitigated models.

### Identify mitigated models¶

The Leaderboard provides several indicators for mitigated and parent
(unmitigated versions) models:

  * A BIAS MITIGATION badge. Use the Leaderboard search to easily identify all mitigated models.

[![](../../../images/bias-mit-6.png)](../../../images/bias-mit-6.png)

  * Model naming reflects mitigation settings (technique, protected feature, and predictor variable status).

[![](../../../images/bias-mit-7.png)](../../../images/bias-mit-7.png)

  * The **Bias Mitigation** tab includes a link to the original, unmitigated parent model.

[![](../../../images/bias-mit-8.png)](../../../images/bias-mit-8.png)

### Compare models¶

Use the [**Bias vs Accuracy**](../../analyze-models/other/bias-tab.html) tab
to compare the bias and accuracy of mitigated vs. unmitigated models. The
chart will likely show that mitigated models have higher fairness scores (less
bias) than their unmitigated version, but with lower accuracy.

[![](../../../images/bias-mit-9.png)](../../../images/bias-mit-9.png)

Before a model (mitigated or unmitigated) becomes available on the chart, you
must first calculate its fairness scores. To compare mitigated or unmitigated:

  1. Open a model displaying the BIAS MITIGATION badge and navigate to [**Bias and Fairness > Per-Class Bias**](../../analyze-models/bias/per-class.html). The fairness score is calculated automatically once you open the tab.

  2. Navigate to the **Bias and Fairness > Bias Mitigation** tab to retrieve a link to the parent model. Click the link to open the parent.

  3. From the parent model, visit the **Bias and Fairness > Per-Class Bias** tab to automatically calculate the fairness score.

  4. Open the [**Bias vs Accuracy**](../../analyze-models/other/bias-tab.html) tab and compare the results. In this example, you can see that the mitigated model (shown in green) has higher accuracy (Y-axis) and fairness (X-axis) scores than the parent (shown in magenta).

[![](../../../images/bias-mit-12.png)](../../../images/bias-mit-12.png)

## Mitigation eligibility¶

DataRobot selects the top three _eligible_ models for mitigation, and as a
result, those labeled with the BIAS MITIGATION badge may not be the top three
models on the Leaderboard after Autopilot runs. Other models may be in a
higher position on the Leaderboard but will not have mitigation applied
because they were ineligible.

If you select **Preprocessing Reweighing** as the mitigation technique, the
following models are ineligible for reweighing because the models don’t use
weights:

  * Nystroem Kernel SVM Classifier
  * Gaussian Process Classifier
  * K-nearest Neighbors Classifier
  * Naive Bayes Classifier
  * Partial Least Squares Classifier
  * Legacy Neural Net models: "vanilla" Neural Net Classifier, Dropout Input Neural Net Classifier, "vanilla" Two Layer Neural Net Classifier, Two Hidden Layer Dropout Rectified Linear Neural Net Classifier, (but note that contemporary Keras models can be mitigated)
  * Certain basic linear models: Logistic Regression, Regularized Logistic Regression (but note that ElasticNet models can be mitigated)
  * Eureqa and Eureqa GAM Classifiers
  * Two-stage Logistic Regression
  * SVM Classifier, with any kernel

If you select either mitigation technique, the following models and/or
projects are ineligible for mitigation:

  * Models that have already had bias mitigation applied.
  * Majority Class Classifier (predicts a constant value).
  * [External Predictions](external-preds.html) models (uses a special column uploaded with the training data, cannot make new predictions).
  * Blender models.
  * Projects using [Smart Downsampling](smart-ds.html).
  * Projects using custom weights.
  * Projects where the **Mitigation Feature** is missing over 50% of its data.
  * Time series or OTV projects (i.e., any project with time-based partitioning).
  * Projects run with [SHAP](../../analyze-models/understand/pred-explain/shap-pe.html) value support.
  * Single-column, standalone text converter models: Auto-Tuned Word N-Gram Text Modeler, Auto-Tuned Char N-Gram Modeler, and Auto-Tuned Summarized Categorical Modeler.

## Bias mitigation considerations¶

Consider the following when working with bias mitigation:

  * Mitigation applies to a single, categorical protected feature.

  * For the **ROBC** mitigation technique, the mitigation feature must have at least two classes that each have at least 100 rows in the training data. For the **Preprocessing Reweighing** technique, there is no explicit minimum row count, but mitigation effectiveness may be unpredictable with very small row counts.

Back to top

