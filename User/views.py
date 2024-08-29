from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User, BlacklistedToken, OTP
from .serializer import UserSerializer, OTPRequestSerializer, OTPVerificationRequestSerializer
from rest_framework.exceptions import NotFound
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import check_password, make_password
from .token import get_token, decode_token_user_id
import bcrypt
from jose import JWTError
import random
import uuid


#_____________________ create user ________________________

@api_view(["POST"])
def create_user(request):
    data = request.data
    data["password"] = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#___________________ user login with OTP ___________________

@api_view(["POST"])
def user_login(request):
    uname = request.data.get("uname")
    password = request.data.get("password")

    if not uname or not password:
        return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(uname=uname)  # Corrected line
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        if not user.is_active:
            return Response({"message": "User account is inactive"}, status=status.HTTP_403_FORBIDDEN)
        
        # Deactivate any existing OTPs
        OTP.objects.filter(user_email=user.email, is_active=True).update(is_active=False, is_deleted=True)

        # Generate a new OTP
        otp_code = str(random.randint(100000, 999999))
        expiration_time = timezone.now() + timedelta(minutes=10)

        # Create the new OTP entry
        OTP.objects.create(
            id=uuid.uuid4(),
            user_email=user.email,
            otp=otp_code,
            expiration_time=expiration_time
        )

        send_otp_email(user.email, otp_code)

        return Response({"message": "OTP sent. Please verify OTP to complete login."}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# send_otp_email

def send_otp_email(email, otp_code):
    subject = "Your OTP Code"
    message = f"Your OTP is {otp_code} which is valid for 10 minutes"
    from_email = 'bhumikadobariya2412@gmail.com'
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Failed to send OTP email: {e}")
        
        
#___________________ verify_otp to complete login ___________________

@api_view(['POST'])
def verify_otp_and_login(request):
    uname = request.data.get("uname")
    otp_code = request.data.get("otp")

    if not uname or not otp_code:
        return Response({"message": "Username and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(uname=uname)
        otp_record = OTP.objects.filter(user=user, otp=otp_code, is_active=True).first()
        if otp_record and otp_record.expiration_time >= timezone.now():
            otp_record.is_active = False
            otp_record.is_deleted = True
            otp_record.save()

            token = get_token(user.id)
            return Response({
                "message": "Login successful",
                "token": token,
                "role": user.role
            }, status=status.HTTP_200_OK)
        return Response({"message": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({"message": "Invalid username"}, status=status.HTTP_404_NOT_FOUND)
    except OTP.DoesNotExist:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_404_NOT_FOUND)
    
    
#___________________user register___________________



@api_view(["POST"])
def user_register(request):
    uname = request.data.get("uname")
    email = request.data.get("email")
    password = request.data.get("password")
    role = request.data.get("role")
    

    if not uname or not email or not password:
        return Response({"message": "Username, email, and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
        user = User.objects.create(
            uname=uname,
            email=email,
            password=hashed_password,
            role=role,
           
        )
        token = get_token(user.id)  
        return Response({
            "message": "User registered and logged in successfully",
            "token": token,
            "role": user.role
        }, status=status.HTTP_201_CREATED)

    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        if not user.is_active:
            return Response({"message": "User account is inactive"}, status=status.HTTP_403_FORBIDDEN)
        token = get_token(user.id) 
        return Response({
            "token": token,
            "role": user.role
        }, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


   
#_______________ get_user_by_id __________________


@api_view(["GET"])

def get_user_by_id(request, id):
    try:
        user = User.objects.get(pk=id, is_active=True, is_deleted=False)
    except User.DoesNotExist:
        raise NotFound(detail="User not found")
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


#__________________ get_user_by_token ________________

@api_view(['GET'])

@api_view(['GET'])
def get_user_by_token(request):
    token = request.headers.get('Authorization')
    if not token:
        return Response({"message": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = decode_token_user_id(token)
        user = User.objects.get(id=user_id)  
        return Response({"email": user.email, "uname": user.uname, "role": user.role}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                        
                        
#_______________ get all user __________________

@api_view(["GET"])
def get_all_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


#______________ update_user_by_id ___________________

@api_view(['PUT'])
def update_user(request, id):
    try:
        user = User.objects.get(pk=id, is_active=True, is_deleted=False)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=False)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#__________________ update_user_by_token ___________________

@api_view(['PUT'])
def update_user_by_token(request):
    token = request.headers.get('Authorization')

    if not token:
        return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user_id_from_token = decode_token_user_id(token)
    except JWTError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(pk=user_id_from_token, is_active=True, is_verified=True, is_deleted=False)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if user_id_from_token != str(user.id):
        return Response({'error': 'Unauthorized to update this user'}, status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#____________ delete_user_by_id _________________

@api_view(['DELETE'])
def delete_user_by_id(request, id):
    try:
        user = User.objects.get(pk=id, is_active=True, is_deleted=False)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.is_active = False
    user.is_deleted = True
    user.save()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


#______________ delete_user_by_token ___________________

@api_view(['DELETE'])
def delete_user_by_token(request):
    token = request.headers.get('Authorization')

    if not token:
        return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user_id_from_token = decode_token_user_id(token)
    except JWTError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(pk=user_id_from_token, is_active=True, is_verified=True, is_deleted=False)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if user_id_from_token != str(user.id):
        return Response({'error': 'Unauthorized to delete this user'}, status=status.HTTP_403_FORBIDDEN)

    user.is_active = False
    user.is_deleted = True
    user.save()

    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


#____________________ logout _____________________

@api_view(["POST"])
def logout(request):
    try:
        access_token = request.data.get('access_token')
        if not access_token:
            return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

        if BlacklistedToken.objects.filter(token=access_token).exists():
            return Response({"message": "Token already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

        BlacklistedToken.objects.create(
            token=access_token,
            blacklisted_at=timezone.now()
        )

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



#__________________forget password by token____________________

@api_view(['PUT'])
def forget_password(request):
    token = request.headers.get('Authorization')
    new_password = request.data.get('user_newpass')

    if not token:
        return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)

    if not new_password:
        return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = decode_token_user_id(token)
    except JWTError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        db_user = User.objects.get(id=user_id, is_active=True, is_verified=True, is_deleted=False)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not db_user.is_verified:
        return Response({'error': 'User not verified'}, status=status.HTTP_403_FORBIDDEN)

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    db_user.password = hashed_password
    db_user.save()
    
    return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)



#___________________reset password by token____________________

@api_view(['PUT'])
def reset_password_by_token(request):
    token = request.headers.get('Authorization')
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not token:
        return Response({'error': 'Token is missing'}, status=status.HTTP_401_UNAUTHORIZED)

    if not old_password or not new_password:
        return Response({'error': 'Old and new passwords are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = decode_token_user_id(token)
    except JWTError:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        db_user = User.objects.get(id=user_id, is_active=True, is_verified=True, is_deleted=False)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not check_password(old_password, db_user.password):
        return Response({'error': 'Old password does not match'}, status=status.HTTP_400_BAD_REQUEST)

    db_user.password = make_password(new_password)
    db_user.save()

    return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)


