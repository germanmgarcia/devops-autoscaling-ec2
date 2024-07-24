output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = [aws_subnet.public_1.id, aws_subnet.public_2.id]
}

output "private_subnet_ids" {
  value = [aws_subnet.private_1.id, aws_subnet.private_2.id]
}

output "alb_dns_name" {
  value = aws_lb.alb.dns_name
}

output "db_instance_endpoint" {
  value = aws_db_instance.example.endpoint
}