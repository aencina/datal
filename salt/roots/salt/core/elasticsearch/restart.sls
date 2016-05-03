elastic_service_restar:
  service.running:
    - enable: True
    - reload: True
    - name: elasticsearch
