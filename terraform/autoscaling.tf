resource "aws_launch_configuration" "app" {
  name          = "example-app"
  image_id      = "ami-007868005aea67c54"
  instance_type = "t2.micro"
  security_groups = [aws_security_group.ec2.id]
  key_name = "terraformec2"
  
  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    amazon-linux-extras install docker -y
    service docker start
    usermod -a -G docker ec2-user
    docker run -d -p 80:80 nginx
  EOF

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "app" {
  launch_configuration = aws_launch_configuration.app.id
  vpc_zone_identifier  = [aws_subnet.private_1.id, aws_subnet.private_2.id]
  min_size             = 1
  max_size             = 3
  desired_capacity     = 1

  target_group_arns = [aws_lb_target_group.example.arn]

  tag {
    key                 = "Name"
    value               = "example-app"
    propagate_at_launch = true
  }
}
