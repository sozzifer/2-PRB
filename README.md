gcloud builds submit --tag gcr.io/stat4002/probability  --project=stat4002

gcloud run deploy --image gcr.io/stat4002/probability --platform managed  --project=stat4002 --allow-unauthenticated