# --------------------------------------------------------
# 1. STORAGE REQUEST (PVC)
# --------------------------------------------------------
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
# --------------------------------------------------------
# 2. DATABASE DEPLOYMENT
# --------------------------------------------------------
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        # Matches the image built by manager.py from Dockerfile-postgres
        image: postgres-db:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 5432

        # Securely Inject Secrets from Kubernetes Secret (db-credentials)
        env:
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: password
        - name: POSTGRES_DB
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: dbname

        # Mount the PVC to the Postgres data directory
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data

      # Define the Volume source
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
---
# --------------------------------------------------------
# 3. NETWORK SERVICE
# --------------------------------------------------------
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  type: ClusterIP
  selector:
    app: postgres
  ports:
    - port: 5432
      targetPort: 5432